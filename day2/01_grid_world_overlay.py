"""
나만의 그리드 월드 만들기 - 할인율에 따른 가치 오버레이

- 그리드 클릭/편집으로 맵 구성 (R=길, T=함정, G=보물, F=가짜보물, S=시작)
- 할인율(γ) 슬라이더로 Value Iteration 결과 실시간 시각화
- 각 셀의 가치(V)를 히트맵으로 오버레이

실행: streamlit run 01_grid_world_overlay.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")

st.set_page_config(page_title="그리드 월드 가치 오버레이", layout="wide")
st.title("🧊 나만의 그리드 월드 만들기")

# S=Start, R=Road, T=Trap, G=Goal, F=Fake treasure
REWARD_MAP = {"S": 0, "R": 0, "T": -100, "G": 100, "F": 10}
TERMINAL_TILES = {"T", "G", "F"}
DISPLAY_GOAL = "💎"
DISPLAY_START = "⚪"


def _to_internal(cell):
    """표시값(💎, ⚪ 등) → 내부 저장값(G, S) 변환"""
    cell = str(cell).strip()
    if cell == DISPLAY_GOAL:
        return "G"
    if cell == DISPLAY_START:
        return "S"
    return cell.upper() if cell else "R"


def parse_grid_to_rewards(grid_df, f_reward=10):
    """그리드 DataFrame → 보상 행렬 (숫자). f_reward: F(가짜보물) 보상값."""
    rows, cols = grid_df.shape
    rewards = np.zeros((rows, cols))
    reward_map = {**REWARD_MAP, "F": f_reward}
    for r in range(rows):
        for c in range(cols):
            cell = _to_internal(grid_df.iloc[r, c])
            rewards[r, c] = reward_map.get(cell, 0)
    return rewards


def is_terminal(grid_df, r, c):
    """해당 셀이 종료 상태(함정/보물)인지"""
    cell = _to_internal(grid_df.iloc[r, c])
    return cell in TERMINAL_TILES


def normalize_tiles(grid_df):
    """g, s, t, r, f, 💎, ⚪ 입력 시 G, S, T, R, F로 변환 (저장값은 항상 알파벳)"""
    if grid_df is None or not isinstance(grid_df, pd.DataFrame):
        return grid_df
    result = grid_df.copy()
    mapping = {"g": "G", "s": "S", "t": "T", "r": "R", "f": "F", DISPLAY_GOAL: "G", DISPLAY_START: "S"}
    for r in range(result.shape[0]):
        for c in range(result.shape[1]):
            cell = str(result.iloc[r, c]).strip()
            result.iloc[r, c] = mapping.get(cell, mapping.get(cell.lower(), cell))
    return result


def to_display_grid(grid_df):
    """내부 그리드(G, S) → 표시용(💎, ⚪) 변환"""
    result = grid_df.copy()
    for r in range(result.shape[0]):
        for c in range(result.shape[1]):
            internal = _to_internal(result.iloc[r, c])
            if internal == "G":
                result.iloc[r, c] = DISPLAY_GOAL
            elif internal == "S":
                result.iloc[r, c] = DISPLAY_START
    return result


def _cell_for_display(cell):
    """셀 값을 표시용으로 (G→💎, S→⚪)"""
    internal = _to_internal(cell)
    if internal == "G":
        return DISPLAY_GOAL
    if internal == "S":
        return DISPLAY_START
    return str(cell).strip()


def enforce_single_sg(edited_df, prev_df):
    """S, G는 각각 1개만 유지. 새로 입력된 셀만 남기고 이전 위치는 R로 복원."""
    if edited_df is None:
        return prev_df.copy() if prev_df is not None else None
    result = edited_df.copy()
    rows, cols = result.shape

    for tile in ("S", "G"):
        # 이전 그리드와 비교해 새로 tile로 바뀐 셀 (가장 마지막 입력 = row-major 마지막)
        changed_to = []
        for r in range(rows):
            for c in range(cols):
                curr = _to_internal(result.iloc[r, c])
                prev = _to_internal(prev_df.iloc[r, c]) if prev_df is not None else ""
                if curr == tile and curr != prev:
                    changed_to.append((r, c))
        if changed_to:
            # 새로 입력된 셀 중 마지막 하나만 유지, 나머지 tile 셀은 R로
            keep_r, keep_c = changed_to[-1]
            for r in range(rows):
                for c in range(cols):
                    if _to_internal(result.iloc[r, c]) == tile and (r, c) != (keep_r, keep_c):
                        result.iloc[r, c] = "R"
    return result


def value_iteration(grid_df, gamma, f_reward=10, max_iters=200):
    """간이 Value Iteration: γ에 따른 각 셀 가치 계산. f_reward: F(가짜보물) 보상값.
    Returns: (V, n_iters_used, converged)"""
    rows, cols = grid_df.shape
    rewards = parse_grid_to_rewards(grid_df, f_reward)
    V = np.zeros((rows, cols))

    # 상 하 좌 우 (행 증감, 열 증감)
    actions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    converged = False
    for i in range(max_iters):
        V_new = V.copy()
        for r in range(rows):
            for c in range(cols):
                if is_terminal(grid_df, r, c):
                    V_new[r, c] = rewards[r, c]
                    continue
                best = -np.inf
                for dr, dc in actions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols:
                        # 다음 칸이 종료 상태면 보상 + 0 (미래 없음)
                        if is_terminal(grid_df, nr, nc):
                            val = rewards[nr, nc]
                        else:
                            val = rewards[nr, nc] + gamma * V[nr, nc]
                    else:
                        val = rewards[r, c] + gamma * V[r, c]  # 맵 밖 → 제자리
                    best = max(best, val)
                V_new[r, c] = best
        # γ가 높을수록 수렴이 느림 → 기준을 엄격히 해서 반복 수 차이가 드러나도록
        if np.allclose(V, V_new, rtol=1e-12, atol=1e-12):
            converged = True
            break
        V = V_new

    return V, i + 1, converged


def get_greedy_path(grid_df, V, gamma, f_reward=10):
    """S에서 시작해 V 기준 그리디하게 이동한 경로 반환 [(r,c), ...]"""
    rows, cols = grid_df.shape
    rewards = parse_grid_to_rewards(grid_df, f_reward)
    actions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # S 위치 찾기
    start = None
    for r in range(rows):
        for c in range(cols):
            if str(grid_df.iloc[r, c]).strip().upper() == "S":
                start = (r, c)
                break
        if start is not None:
            break
    if start is None:
        return []

    path = [start]
    max_steps = rows * cols
    for _ in range(max_steps):
        r, c = path[-1]
        if is_terminal(grid_df, r, c):
            break
        best_val, best_next = -np.inf, None
        for dr, dc in actions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if is_terminal(grid_df, nr, nc):
                    val = rewards[nr, nc]
                else:
                    val = rewards[nr, nc] + gamma * V[nr, nc]
                next_pos = (nr, nc)
            else:
                val = rewards[r, c] + gamma * V[r, c]
                next_pos = (r, c)
            if val > best_val:
                best_val = val
                best_next = next_pos
        if best_next is None or best_next == path[-1]:
            break
        path.append(best_next)
    return path


# 1. 사이드바 설정
with st.sidebar:
    st.header("⚙️ 설정")
    gamma = st.slider("할인율 γ (Gamma)", 0.0, 0.99, 0.9, 0.01)
    f_reward = st.slider("가짜 보물(F) 보상", 10, 100, 10, 5)
    rows = st.number_input("행 (Row)", 3, 10, 4, 1)
    cols = st.number_input("열 (Col)", 3, 10, 4, 1)
    max_t_and_f = max(0, rows * cols - 2)

    # 함정/가짜보물 수 유지: trap+fake <= n*m-2, 넘치면 가짜 먼저 줄이고 그래도 넘치면 함정도 줄임
    prev_trap = st.session_state.get("last_trap_count", 0)
    prev_fake = st.session_state.get("last_fake_count", 0)
    if prev_trap + prev_fake > max_t_and_f:
        new_fake = max(0, max_t_and_f - prev_trap)
        new_trap = max_t_and_f - new_fake
    else:
        new_trap, new_fake = prev_trap, prev_fake

    trap_count = st.slider("함정 수 (Trap)", 0, max_t_and_f, new_trap, 1)
    max_fake = max(0, max_t_and_f - trap_count)
    fake_default = min(new_fake, max_fake)
    fake_count = st.slider("가짜 보물 수 (F)", 0, max_fake, fake_default, 1)

    st.session_state.last_trap_count = trap_count
    st.session_state.last_fake_count = fake_count
    if st.button("🔄 리셋"):
        if "grid" in st.session_state:
            del st.session_state.grid
        st.session_state.editor_key = st.session_state.get("editor_key", 0) + 1
        st.rerun()


# 2. 그리드 상태 관리
needs_init = "grid" not in st.session_state
if "grid" in st.session_state and st.session_state.grid.shape != (rows, cols):
    needs_init = True
if "grid" in st.session_state and (
    st.session_state.get("init_trap_count") != trap_count
    or st.session_state.get("init_fake_count") != fake_count
):
    needs_init = True
if needs_init:
    default = [["R"] * cols for _ in range(rows)]
    positions = [(r, c) for r in range(rows) for c in range(cols)]
    np.random.shuffle(positions)
    idx = 0
    for _ in range(trap_count):
        if idx < len(positions):
            r, c = positions[idx]
            default[r][c] = "T"
            idx += 1
    for _ in range(fake_count):
        if idx < len(positions):
            r, c = positions[idx]
            default[r][c] = "F"
            idx += 1
    # R인 셀 중 랜덤으로 시작점(S), 보물(G) 각 1개 배치
    r_positions = [(r, c) for r in range(rows) for c in range(cols) if default[r][c] == "R"]
    start_idx, goal_idx = np.random.choice(len(r_positions), size=2, replace=False)
    default[r_positions[start_idx][0]][r_positions[start_idx][1]] = "S"
    default[r_positions[goal_idx][0]][r_positions[goal_idx][1]] = "G"
    st.session_state.grid = pd.DataFrame(default, columns=[str(i) for i in range(cols)])
    st.session_state.init_trap_count = trap_count
    st.session_state.init_fake_count = fake_count

if "editor_key" not in st.session_state:
    st.session_state.editor_key = 0

st.info("셀을 **더블클릭**해서 편집하세요: R(길), T(함정, -100), G(보물💎, +100), F(가짜보물), S(시작⚪)")

# 3. 그리드 에디터 + 가치 히트맵 + 최적 경로
col_grid, col_heat, col_path = st.columns(3)

with col_grid:
    st.subheader("📋 그리드 에디터")
    prev_grid = st.session_state.grid.copy()
    edited_grid = st.data_editor(
        to_display_grid(st.session_state.grid),
        key=f"grid_editor_{st.session_state.editor_key}",
        height=350,
        width="stretch",
        column_config={c: st.column_config.TextColumn(c, width="small") for c in st.session_state.grid.columns}
    )
    if edited_grid is None:
        edited_grid = prev_grid
    else:
        edited_grid = normalize_tiles(edited_grid)
        edited_grid = prev_grid if edited_grid is None else edited_grid
        edited_grid = enforce_single_sg(edited_grid, prev_grid)
        edited_grid = prev_grid if edited_grid is None else edited_grid
    st.session_state.grid = edited_grid
    # 정규화/SG강제 적용 시 셀에 반영되도록 rerun (data_editor는 포커스 아웃 시 반환)
    if not edited_grid.equals(prev_grid):
        st.rerun()

with col_heat:
    st.subheader("📊 가치(V) 히트맵")
    try:
        V, n_iters, converged = value_iteration(edited_grid, gamma, f_reward, max_iters=2000)


        fig, ax = plt.subplots(figsize=(5, 4))
        im = ax.imshow(V, cmap="RdYlGn", aspect="auto")

        # 셀에 값 표시
        for r in range(V.shape[0]):
            for c in range(V.shape[1]):
                text = f"{V[r, c]:.2f}" if not is_terminal(edited_grid, r, c) else "END"
                ax.text(c, r, text, ha="center", va="center", fontsize=9, fontweight="bold")

        ax.set_xticks(np.arange(V.shape[1]))
        ax.set_yticks(np.arange(V.shape[0]))
        ax.set_xticklabels(np.arange(V.shape[1]))
        ax.set_yticklabels(np.arange(V.shape[0]))
        ax.set_xlabel("Col")
        ax.set_ylabel("Row")
        plt.colorbar(im, ax=ax, label="V(s)")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
        if converged:
            if n_iters >= 200:
                st.markdown(f':yellow[⚠️ 반복 {n_iters}회 — 할인율이 높아 수렴에 오래 걸렸습니다.]')
            else:
                st.caption(f"반복 {n_iters}회 ✓ 수렴")
        else:
            st.caption(f"반복 {n_iters}회 (미수렴)")
    except Exception as e:
        st.error(f"가치 계산 오류: {e}")

with col_path:
    st.subheader("🎯 최적 경로 (S→G)")
    try:
        V, _, converged = value_iteration(edited_grid, gamma, f_reward, max_iters=2000)
        path = get_greedy_path(edited_grid, V, gamma, f_reward)
        path_set = set(path)

        fig, ax = plt.subplots(figsize=(5, 4))
        ax.imshow(np.zeros((edited_grid.shape[0], edited_grid.shape[1])), cmap="Greys", aspect="auto", vmin=0, vmax=1)
        for r in range(edited_grid.shape[0]):
            for c in range(edited_grid.shape[1]):
                cell = _to_internal(edited_grid.iloc[r, c])
                if (r, c) in path_set:
                    step = path.index((r, c))
                    ax.add_patch(plt.Rectangle((c - 0.5, r - 0.5), 1, 1, fill=True, facecolor="yellow", alpha=0.5, edgecolor="red", linewidth=2))
                    ax.text(c, r, str(step), ha="center", va="center", fontsize=10, fontweight="bold")
                else:
                    ax.text(c, r, cell, ha="center", va="center", fontsize=9)
        for i in range(len(path) - 1):
            r0, c0 = path[i]
            r1, c1 = path[i + 1]
            ax.annotate("", xy=(c1, r1), xytext=(c0, r0), arrowprops=dict(arrowstyle="->", color="red", lw=2))
        ax.set_xticks(np.arange(edited_grid.shape[1]))
        ax.set_yticks(np.arange(edited_grid.shape[0]))
        ax.set_xticklabels(np.arange(edited_grid.shape[1]))
        ax.set_yticklabels(np.arange(edited_grid.shape[0]))
        ax.set_xlabel("Col")
        ax.set_ylabel("Row")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
        if path:
            dest_internal = _to_internal(edited_grid.iloc[path[-1][0], path[-1][1]])
            warn = " (⚠ 미수렴 시 부정확)" if not converged else ""
            st.caption(f"경로: {len(path)}칸 → {dest_internal}{warn}")
    except Exception as e:
        st.error(f"경로 계산 오류: {e}")

st.caption(
    "**γ 낮음** (0.3-0.6): 단기 보상 선호 → 가까운 F로 최적 경로가 바뀔 수 있음. "
    "**γ 높음** (0.95-1.0): 먼 미래까지 고려하지만, Value Iteration 수렴에 많은 반복 필요 → 반복 수 부족 시 잘못된 경로 표시."
)
