import time
import pygame
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

pygame.init()
pygame.display.set_caption("Whatsapp-Bot")
window = pygame.display.set_mode((500, 500))
window.fill((0, 0, 0))
pygame.display.update()
wait_img = pygame.transform.scale(pygame.image.load("./wait.png"), (500, 500))

def screenshot_qrcode():
    element = driver.find_element_by_tag_name('canvas')
    element.screenshot('qrcode.png')

def display_qrcode():
    img = pygame.transform.scale(pygame.image.load("./qrcode.png"), (500, 500))
    window.blit(img, (0, 0))
    pygame.display.update()

def display_holdon():
    window.blit(wait_img, (0, 0))
    pygame.display.update()

options = Options()
options.headless = True
# that executable maybe works on linux, but certainly not on windows
# TODO: support for Linux/Windows
driver = webdriver.Firefox(options=options, executable_path='./geckodriver')
driver.get("https://web.whatsapp.com/")

prev_time = time.time()
time_passed = 0
clock = pygame.time.Clock()

display_holdon()

# TODO: not use the >event based< (wich means it needs a loop to run) pygame, but a more lightweight solution
# this also enables a simpler and more readable implementation for the multiple waiting times

run = True
while run:
    clock.tick(4)
    now = time.time()
    delta_time = now - prev_time
    prev_time = now
    time_passed += delta_time

    # TODO: instead of hardcoding the waiting time, check the pages loading status / the qr-codes canvas for updates

    # basic timetable:
    # 0 - 5   waiting screen (page loads)
    # 5 - 10  qr-code 1 is displayed
    # 10 - 15 waiting screen (whatsapp generates new qr-code)
    # 15 - 20 qr-code 2 is displayed
    # 20 - 30 whatsapp web loads
    # as said, replace this with something more dynamical

    if round(time_passed) == 5 or round(time_passed) == 15:
        screenshot_qrcode()
        display_qrcode()
    elif round(time_passed) == 10 or round(time_passed) == 20:
        display_holdon()
    elif round(time_passed) == 30:
        run = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

def setChat(substring):
    driver.find_element_by_xpath(f"//*[text()[contains(., '{substring}')]]").click()
    # You wanna know how i figured this out? That was a year ago and i have no idea. It works though.

def sendMessage(message):
    actions = ActionChains(driver)
    actions.send_keys(message)
    actions.send_keys(Keys.ENTER)
    actions.perform()

setChat("ChatOrGroupsubstring")
sendMessage("message")
