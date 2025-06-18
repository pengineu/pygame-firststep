import pygame, math, sys, random

pygame.init()
screen = pygame.display.set_mode((1366, 768))
pygame.display.set_caption("Cannon The Penguin!")
clock = pygame.time.Clock()

def ingame():
    # 게임에서 사용될 여러 변수 설정/초기화
    x, y = 375, 600
    cannon_speed = 0
    acceleration = 0.01
    max_speed = 3
    angle = 0
    wheel_angle = 0
    angle_da = (math.pi * 2) / 5
    charge = False
    shooting = False
    shoot_angle = math.radians(45)
    charging_gauge = 20
    charging_tick = 1
    vx = 0
    vy = 0
    air_resistence = random.randint(9992, 10008) / 10000
    gravity = 0.98
    cannon_ball_x = 0
    cannon_ball_y = 0
    camera_x = 0
    camera_y = 768 * -15
    seal_x = 1366 * 10 + random.randint(-1366*5, 1366*5)
    seal_y = 768 * -15.5
    moving_x = 0
    moving_y = 0
    cannonball_count = 5
    shoot_sound = pygame.mixer.Sound("./025_터지는소리BOOM.WAV")
    attack_sound = pygame.mixer.Sound("./019_퓨히익 (online-audio-converter.com) (1).wav")

    cannonball_image = pygame.image.load("./cannonball.png")
    cannonball_image = pygame.transform.scale(cannonball_image, (100, 100))
    seal_image = pygame.image.load("./물범.png")
    seal_image = pygame.transform.scale(seal_image, (1366, 768))
    wheel_image = pygame.image.load("./바퀴 이미지.png")
    cannon_image = pygame.image.load("./대포이미지-removebg-preview-plusplu.png")
    background_image = pygame.image.load("./펭귄배경.png")
    background_image = pygame.transform.scale(background_image, (1366*16, 768*16)) # 배경을 매우 크게 설정

    running = True
    screen_moving = False

    # 파이게임 루프
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # 대포 차징
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                charge = True

            if charge:
                charging_gauge += charging_tick
            # 대포 발사
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE and charge:
                shoot_sound.play()
                charge = False
                shooting = True
                force = min(charging_gauge, 10000)
                vx = force * math.cos(shoot_angle * math.pi / 180) # 대포 각도와 연관된 힘 분해
                vy = -force * math.sin(shoot_angle * math.pi / 180)
                charging_gauge = 20 # 다음 발사를 위한 차징 게이지 초기화
                cannon_ball_x = x
                cannon_ball_y = y
                cannonball_count -= 1 # 발사 횟수 제한

            # w, a, s, d키를 이용한 게임 화면 이동
            if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                screen_moving = True
                moving_x -= 25

            if event.type == pygame.KEYUP and event.key == pygame.K_d:
                screen_moving = True
                moving_x += 25

            if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                screen_moving = True
                moving_y += 25

            if event.type == pygame.KEYUP and event.key == pygame.K_w:
                screen_moving = True
                moving_y -= 25

            if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                screen_moving = True
                moving_x += 25

            if event.type == pygame.KEYUP and event.key == pygame.K_a:
                screen_moving = True
                moving_x -= 25

            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                screen_moving = True
                moving_y -= 25

            if event.type == pygame.KEYUP and event.key == pygame.K_s:
                screen_moving = True
                moving_y += 25
            # m 키를 누르면 원위치
            if event.type == pygame.KEYUP and event.key == pygame.K_m:
                screen_moving = False
                camera_x = 0
                camera_y = 768 * -15

        if screen_moving:
            camera_x += moving_x
            camera_y += moving_y
        else:
            moving_x = 0
            moving_y = 0

        screen.fill((255, 255, 255))
        screen.blit(background_image, (camera_x - 375*2, camera_y + 400))

        if cannonball_count == 0 and not shooting:
            return outgame()


        # 대포 발사, 카메라 이동을 하면 대포가 안보이도록 대포 삭제(반대로 발사, 카메라 이동이 아닐 때 대포가 보이도록 구현)
        if not shooting and not screen_moving:
            rotated_cannon = pygame.transform.rotate(cannon_image, -angle)
            cannon_rect = rotated_cannon.get_rect(center=(x, y))
            screen.blit(rotated_cannon, cannon_rect)

            rotated_wheel = pygame.transform.rotate(wheel_image, -wheel_angle)
            wheel_rect = rotated_wheel.get_rect(center=(x, y))
            screen.blit(rotated_wheel, wheel_rect)

            pygame.draw.rect(screen, (0, 255, 0), (camera_x, camera_y + 768*15 + 768//4, (charging_gauge - 20)*2, 20)) # 차징 게이지 바 구현

            for i in range(1, cannonball_count + 1): # 150*i 를 간격으로 cannonball count 보여주기
                cannonballcount_rect = cannonball_image.get_rect(center=(camera_x + 1366//4 + 150*i, camera_y + 768*15 + 50))
                screen.blit(cannonball_image, cannonballcount_rect)

            pygame.draw.rect(screen, (0, 0, 0), (camera_x, camera_y + 768*15 , 1366 // 4, 768 // 4)) # 미니맵
            pygame.draw.circle(screen, (255, 0, 0), (camera_x + (camera_x + seal_x) // 64, camera_y + 768*15 + (-seal_y) // 64), 8) # 물범 위치
            pygame.draw.circle(screen, (0, 0, 255), (x // 64, (+cannon_ball_y) // 64 + 768 // 4 - 8), 8) # 대포 위치
            wind_speed = air_resistence - 1
            if air_resistence > 1:
                pygame.draw.rect(screen, (255, 0, 0), (camera_x + 1366//8, camera_y + 768*15 + 768//4 + 20, wind_speed*100000, 20))
            elif air_resistence < 1:
                pygame.draw.rect(screen, (0, 0, 255), (camera_x + 1366//8 - -wind_speed*100000, camera_y + 768*15 + 768//4 + 20, -wind_speed*100000, 20))
        # 대포 발사중
        if shooting:
            vx *= 0.999
            vx += wind_speed * 500
            vy += gravity
            cannon_ball_x += vx
            cannon_ball_y += vy
            cannonball_rect = cannonball_image.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2)) # 대포알을 화면 중앙에 위치
            screen.blit(cannonball_image, cannonball_rect)
            camera_x = -cannon_ball_x + screen.get_width() // 2 # 대포알이 아닌 배경을 이동
            camera_y = -cannon_ball_y + screen.get_height() // 2 - 768 * 15
            x -= vx
            y -= vy
            pygame.draw.rect(screen, (0, 0, 0), (0, 0, 1366 // 4, 768 // 4)) # 미니맵
            pygame.draw.circle(screen, (255, 0, 0), ((seal_x) // 64,(-seal_y) // 64), 8) # 물범 위치
            pygame.draw.circle(screen, (0, 0, 255), (cannon_ball_x // 64, (+cannon_ball_y) // 64 + 768 // 4 - 16), 8) # 대포알 위치

            if cannonball_rect.colliderect(seal_rect): # 대포알과 표적의 충돌 이벤트
                attack_sound.play()
                return endgame()

            if camera_x < -1366 * 15 or camera_y < 768 * -15.5: # 배경 밖으로 나가지 않도록 설정, 객체를 못 맞춘 경우로 간주, 변수 초기화
                shooting = False
                camera_x = 0
                camera_y = 768 * -15
                x, y = 375, 600
                cannon_ball_x = 0
                cannon_ball_y = 0
                air_resistence = random.randint(9992, 10008) / 10000

        keys = pygame.key.get_pressed()

        # 대포의 이동
        if keys[pygame.K_LEFT]:
            cannon_speed = max(cannon_speed - acceleration, -max_speed)
            if cannon_speed > 0:
                cannon_speed -= acceleration # 가속도 구현
            wheel_angle -= angle_da # 바퀴가 돌아가는 각도
        elif keys[pygame.K_RIGHT]:
            cannon_speed = min(cannon_speed + acceleration, max_speed)
            if cannon_speed < 0:
                cannon_speed += acceleration
            wheel_angle += angle_da
        elif cannon_speed != 0:
            cannon_speed -= cannon_speed / abs(cannon_speed) * acceleration # 가속도 물리엔진 구현
            # 대포 발사 각도 조절
        if keys[pygame.K_UP]:
            angle -= angle_da
        if keys[pygame.K_DOWN]:
            angle += angle_da
        x += cannon_speed
        # 대포 발사 각도 제한
        angle = min(angle, 45)
        angle = max(-45, angle)
        shoot_angle = (-angle + 45)

        seal_rect = seal_image.get_rect(center=(camera_x + seal_x, camera_y - seal_y))
        screen.blit(seal_image, seal_rect)



        pygame.display.flip()
        clock.tick(60)


    pygame.quit()
    sys.exit()

def endgame():
    running = True

    background_image = pygame.image.load("./게임클리어background.png")
    background_image = pygame.transform.scale(background_image, (1366, 768))
    gameclear_image = pygame.image.load("./게임클리어.png")
    gameclear_image = pygame.transform.scale(gameclear_image, (1366, 768))

    # 파이게임 루프

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return ingame()

        screen.fill((255, 255, 255))
        screen.blit(background_image, (0, 0))

        gameclear_rect = gameclear_image.get_rect(center=(screen.get_width() // 2 , screen.get_height() // 2))
        screen.blit(gameclear_image, gameclear_rect)
        pygame.display.flip()
        clock.tick(60)


def startgame():
    running = True

    background_image = pygame.image.load("./펭귄배경.png")
    background_image = pygame.transform.scale(background_image, (1366, 768))
    startmessage_image = pygame.image.load("./제목.png")
    startmessage_image = pygame.transform.scale(startmessage_image, (1366, 768))
    # 파이게임 루프
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return ingame()

        screen.fill((255, 255, 255))
        screen.blit(background_image, (0, 0))
        startmessage_rect = startmessage_image.get_rect(center=(screen.get_width() // 2 + 100, screen.get_height() // 2))
        screen.blit(startmessage_image, startmessage_rect)

        pygame.display.flip()
        clock.tick(60)


def outgame():
    running = True

    background_image = pygame.image.load("./펭귄배경.png")
    background_image = pygame.transform.scale(background_image, (1366, 768))
    gameover_image = pygame.image.load("./게임오버.png")
    gameover_image = pygame.transform.scale(gameover_image, (1366, 768))
    # 파이게임 루프
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return ingame()

        screen.fill((255, 255, 255))
        screen.blit(background_image, (0, 0))

        gameover_rect = gameover_image.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(gameover_image, gameover_rect)

        pygame.display.flip()
        clock.tick(60)

startgame()


