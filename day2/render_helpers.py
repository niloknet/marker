"""
Gymnasium 환경 렌더링 + 보상 오버레이

rgb_array 모드 환경을 pygame 창에 표시하고, 보상값을 오버레이합니다.
"""

import pygame
import numpy as np


def init_display(frame_shape):
    """프레임 크기로 pygame 디스플레이 초기화. (H, W, 3) → width, height"""
    h, w = frame_shape[0], frame_shape[1]
    pygame.init()
    screen = pygame.display.set_mode((w, h))
    return screen


def render_frame_with_overlay(env, screen, step_reward, total_reward, episode=None):
    """
    env에서 프레임을 받아 pygame 화면에 그리고, 보상 오버레이를 추가.
    env는 render_mode="rgb_array"여야 함.
    """
    frame = env.render()
    if frame is None:
        return
    # numpy (H, W, 3) → pygame (W, H, 3)
    frame = np.transpose(frame, (1, 0, 2))
    surf = pygame.surfarray.make_surface(frame)
    screen.blit(surf, (0, 0))

    # 보상 텍스트 (흰색, 검은 테두리)
    font = pygame.font.Font(None, 32)
    lines = [
        f"Step reward: {step_reward:.2f}",
        f"Total: {total_reward:.1f}",
    ]
    if episode is not None:
        lines.insert(0, f"Episode: {episode}")
    y = 10
    for line in lines:
        text = font.render(line, True, (255, 255, 255))
        # 테두리
        for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            outline = font.render(line, True, (0, 0, 0))
            screen.blit(outline, (11 + dx, y + dy))
        screen.blit(text, (10, y))
        y += 24
    pygame.display.flip()


_clock = None


def check_user_stop():
    """키 입력 또는 창 닫기 시 True 반환 (상호작용 감지)"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
        if event.type == pygame.KEYDOWN:
            return True
        if event.type == pygame.MOUSEBUTTONDOWN:
            return True
    return False


def tick_fps(env):
    """환경 메타데이터의 render_fps에 맞춰 대기"""
    global _clock
    if _clock is None:
        _clock = pygame.time.Clock()
    fps = env.metadata.get("render_fps", 50)
    _clock.tick(fps)
