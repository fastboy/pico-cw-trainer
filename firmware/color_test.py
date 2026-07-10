from display import Display
import st7789

d = Display()

d.tft.fill(st7789.BLACK)

d.tft.fill_rect(10, 10, 40, 40, st7789.RED)
d.tft.fill_rect(60, 10, 40, 40, st7789.GREEN)
d.tft.fill_rect(110, 10, 40, 40, st7789.BLUE)
d.tft.fill_rect(160, 10, 40, 40, st7789.YELLOW)
d.tft.fill_rect(210, 10, 40, 40, st7789.CYAN)
