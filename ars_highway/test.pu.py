MAX_LANE_SPEED = 30

def getSpeedReward(speed):
    return (-1 * (1 / (MAX_LANE_SPEED / (6 / 7))) * speed ** 7 + speed ** 6)


def getCurrentSpeedReward(speed):
    return (10 / getSpeedReward(MAX_LANE_SPEED)) * getSpeedReward(speed)

print(getCurrentSpeedReward(15))
print(getCurrentSpeedReward(30))
print(getCurrentSpeedReward(35))