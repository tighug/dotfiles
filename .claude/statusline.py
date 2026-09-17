#!/usr/bin/env python3
"""Claude Code status line: cwd, git branch, model, context usage, rate limits
with braille progress bars"""
import json
import os
import sys
from pathlib import Path

BRAILLE = ' ⣀⣄⣤⣦⣶⣷⣿'
R = '\033[0m'           # 全属性リセット（行全体の始点・終点でのみ使う）
FR = '\033[22;39m'      # dim/前景色だけをリセットし背景色は残す（セグメント内部用）

ICON_BRANCH = ''      # nf-dev-git_branch
ICON_MODEL = '\U000f167a'   # nf-md-robot_outline
LEFT_CAP = ''         # nf-ple-left_half_circle_thick
RIGHT_CAP = ''        # nf-ple-right_half_circle_thick

# 24bit 色前提（~/.zshrc の COLORTERM=truecolor）。未設定だと 256 色に丸められ、
# 暗い青系は濃紺 #00005f に化ける
WHITE_FG = '\033[38;2;200;204;212m'    # 未知モデルの文字色
DIR_FG = '\033[38;2;86;182;194m'       # CWD の文字色（One Dark cyan）
BRANCH_FG = '\033[38;2;224;108;117m'   # ブランチの文字色（One Dark red）
LABEL_FG = '\033[38;2;130;137;151m'    # ctx/5h/7d のラベル文字色（控えめ）
EMPTY_FG = '\033[38;2;92;99;112m'      # バーの空きマスの色（背景より少し明るいグレー）
EMPTY_CELL = '⣀'

# One Dark 背景 #282c34 を少し明るくした2段階を交互に使い、濃淡の差で区切りを示す
SHADES = [(53, 58, 69), (64, 70, 83)]
MODEL_COLORS = {
    'opus': '\033[38;2;196;150;255m',
    'sonnet': '\033[38;2;110;180;255m',
    'haiku': '\033[38;2;120;215;150m',
    'fable': '\033[38;2;240;200;100m',
}


def bg_esc(rgb):
    r, g, b = rgb
    return f'\033[48;2;{r};{g};{b}m'


def fg_esc(rgb):
    r, g, b = rgb
    return f'\033[38;2;{r};{g};{b}m'


def render(contents):
    """内容のリストを1本の連続したピルとして描画する。
    丸キャップは両端だけで、セグメント間は SHADES の濃淡切り替えで区切る"""
    if not contents:
        return ''
    shades = [SHADES[i % len(SHADES)] for i in range(len(contents))]
    out = fg_esc(shades[0]) + LEFT_CAP + R
    for bg, content in zip(shades, contents):
        out += bg_esc(bg) + ' ' + content + ' '
    out += R + fg_esc(shades[-1]) + RIGHT_CAP + R
    return out


def gradient(pct):
    """緑→黄→赤のグラデーション色コードを返す"""
    if pct < 50:
        r = int(pct * 5.1)
        return f'\033[38;2;{r};200;80m'
    else:
        g = int(200 - (pct - 50) * 4)
        return f'\033[38;2;255;{max(g, 0)};60m'


def braille_bar(pct, width=4):
    """ブライユ点字のバーを (埋まった部分の文字列, 空きマス数) で返す"""
    pct = min(max(pct, 0), 100)
    level = pct / 100
    filled = ''
    empty = 0
    for i in range(width):
        seg_start = i / width
        seg_end = (i + 1) / width
        if level >= seg_end:
            filled += BRAILLE[7]
            continue
        idx = 0 if level <= seg_start else min(int((level - seg_start) / (seg_end - seg_start) * 7), 7)
        if idx == 0:
            empty += 1
        else:
            filled += BRAILLE[idx]
    return filled, empty


def fmt_bar(label, pct):
    """ラベル + プログレスバー + パーセント表示を返す（セグメント内部用、末尾はFRのみ）"""
    p = round(pct)
    color = gradient(pct)
    filled, empty = braille_bar(pct)
    return (f'{LABEL_FG}{label}{FR} {color}{filled}{EMPTY_FG}{EMPTY_CELL * empty}'
            f'{color} {p}%{FR}')


def short_model(display_name):
    """モデルの display_name からファミリ略称と文字色を返す"""
    name = (display_name or '').lower().strip()
    for family, color in MODEL_COLORS.items():
        if name.startswith(family):
            return family, color
    first = name.split()[0] if name.split() else 'claude'
    return first, WHITE_FG


def dir_name(current_dir):
    """現在のディレクトリ名だけを返す（ホームは ~、ルートは /）"""
    if current_dir == str(Path.home()):
        return '~'
    return os.path.basename(current_dir.rstrip('/')) or '/'


def _read_head_ref(head_file):
    try:
        with open(head_file) as f:
            head = f.read().strip()
    except OSError:
        return None
    if head.startswith('ref: refs/heads/'):
        return head[len('ref: refs/heads/'):]
    return head[:7] if head else None  # detached HEAD: short SHA


def _resolve_git_dir(git_path):
    """.git がディレクトリならそのまま、ファイル（worktree）なら gitdir: を辿る"""
    if os.path.isdir(git_path):
        return git_path
    try:
        with open(git_path) as f:
            content = f.read().strip()
    except OSError:
        return None
    if not content.startswith('gitdir:'):
        return None
    gitdir = content[len('gitdir:'):].strip()
    if not os.path.isabs(gitdir):
        gitdir = os.path.join(os.path.dirname(git_path), gitdir)
    return gitdir


def find_git_branch(current_dir):
    """current_dir から上に辿って .git/HEAD を直接読む（サブプロセスなし）"""
    d = current_dir
    while True:
        git_path = os.path.join(d, '.git')
        if os.path.exists(git_path):
            git_dir = _resolve_git_dir(git_path)
            if git_dir is None:
                return None
            return _read_head_ref(os.path.join(git_dir, 'HEAD'))
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent


def git_branch(data, current_dir):
    """Claude 管理ワークツリー内なら payload の worktree.branch を優先"""
    wt_branch = data.get('worktree', {}).get('branch')
    if wt_branch:
        return wt_branch
    return find_git_branch(current_dir)


def main():
    data = json.load(sys.stdin)

    segments = []

    workspace = data.get('workspace', {})
    current_dir = workspace.get('current_dir') or data.get('cwd')
    if current_dir:
        segments.append(f'{DIR_FG}{dir_name(current_dir)}{FR}')
        branch = git_branch(data, current_dir)
        if branch:
            segments.append(f'{BRANCH_FG}{ICON_BRANCH} {branch}{FR}')

    display_name = data.get('model', {}).get('display_name')
    if display_name:
        abbr, color = short_model(display_name)
        segments.append(f'{color}{ICON_MODEL} {abbr}{FR}')

    ctx = data.get('context_window', {}).get('used_percentage')
    if ctx is not None:
        segments.append(fmt_bar('ctx', ctx))

    five = data.get('rate_limits', {}).get('five_hour', {}).get('used_percentage')
    if five is not None:
        segments.append(fmt_bar('5h', five))

    week = data.get('rate_limits', {}).get('seven_day', {}).get('used_percentage')
    if week is not None:
        segments.append(fmt_bar('7d', week))

    print(render(segments), end='')


def _selftest():
    """assert ベースの自己テスト（フレームワークなし）"""
    import tempfile

    # short_model: 既知ファミリ / 未知モデル
    assert short_model('Opus 5 (1M context)')[0] == 'opus'
    assert short_model('Sonnet 4.6')[0] == 'sonnet'
    assert short_model('Haiku 3.5')[0] == 'haiku'
    assert short_model('Fable 5.1')[0] == 'fable'
    assert short_model('SomeFutureModel X')[0] == 'somefuturemodel'
    assert short_model(None)[0] == 'claude'

    # dir_name: ホーム / 深いパス / 末尾スラッシュ / ルート
    home = str(Path.home())
    assert dir_name(home) == '~'
    assert dir_name(f'{home}/w/deep/proj') == 'proj'
    assert dir_name('/tmp/') == 'tmp'
    assert dir_name('/') == '/'

    # git_branch: 通常リポジトリ / detached HEAD / worktree.branch 優先
    with tempfile.TemporaryDirectory() as tmp:
        git_dir = os.path.join(tmp, '.git')
        os.makedirs(git_dir)
        with open(os.path.join(git_dir, 'HEAD'), 'w') as f:
            f.write('ref: refs/heads/main\n')
        sub = os.path.join(tmp, 'a', 'b')
        os.makedirs(sub)
        assert find_git_branch(sub) == 'main'

        with open(os.path.join(git_dir, 'HEAD'), 'w') as f:
            f.write('a1b2c3d4e5f6\n')
        assert find_git_branch(tmp) == 'a1b2c3d'

        assert git_branch({'worktree': {'branch': 'feature/x'}}, tmp) == 'feature/x'

    assert find_git_branch('/nonexistent/path/xyz') is None

    # braille_bar: 空・満杯・途中（埋まり + 空き = 幅）
    assert braille_bar(0) == ('', 4)
    assert braille_bar(100) == ('⣿' * 4, 0)
    f, e = braille_bar(50)
    assert (f, e) == ('⣿⣿', 2)

    # render: 空リストは空文字列、複数セグメントでも丸キャップは始点・終点に1個ずつだけ
    assert render([]) == ''
    multi = render(['a', 'b', 'c'])
    assert multi.count(LEFT_CAP) == 1
    assert multi.count(RIGHT_CAP) == 1
    # 隣り合うセグメントは必ず異なる背景色になる
    import re
    bgs = re.findall(r'\033\[48;2;([\d;]+)m', multi)
    assert len(bgs) == 3 and bgs[0] != bgs[1] and bgs[1] != bgs[2]

    # 欠損耐性: ペイロードが空でも例外を出さない
    import io
    import contextlib
    old_stdin = sys.stdin
    try:
        sys.stdin = io.StringIO('{}')
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            main()
        assert buf.getvalue() == ''
    finally:
        sys.stdin = old_stdin

    print('OK', file=sys.stderr)


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        _selftest()
    else:
        main()
