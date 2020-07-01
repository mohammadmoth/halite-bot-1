import hlt
import logging
import random
from collections import OrderedDict
game = hlt.Game("Faster -V4")
logging.info("Starting my Faster bot!")
ignore_planttacksame = False
AttackOwnerPlanet = False
turn = 0
while True:
    turn = turn + 1
    #logging.info("turn :" + str(turn))
    Map = game.update_map()
    commands = []
    Planet_has_been_attacked = []
    """
    الخطة

    لا يقوم بالهجوم على نفس الكوكب اكثر من مره بنفس الفريم


    قرار احتلال العدو او الكواكب الفارغة يعتمد على عدد الكواكب المحتلة
    في حال كان احتل نسبة تصل 40% من لعبة يقوم بتجميع القوات والتنقل من كوكب الى كوكب للاحتال السريع


    تطويرات اضافية 
    البحث عن سفن العدو 
    سفني المصابة تنسحب الى مكان امن للمعالجة في كوكب ما
    اقلاع السفن من الكوكب و الهجوم
    """
    alltroops = Map.get_me().all_ships()
    listofplantdock = []
    for arrmy in alltroops:

        targetplanet = []
        targetarrmy = []

        if arrmy.docking_status != arrmy.DockingStatus.UNDOCKED:
            continue

        entities_by_distance_all = Map.nearby_entities_by_distance(arrmy)

        entities_by_distance_all = sorted(entities_by_distance_all.items(
        ), key=lambda entities_by_distance_allX: entities_by_distance_allX[0], reverse=False)

        for target in entities_by_distance_all:
            if isinstance(target[1][0], hlt.entity.Planet) and (not target[1][0].is_owned() or AttackOwnerPlanet):
                targetplanet.append(target[1][0])

          #  else:
          #      logging.info()

       # logging.info(targetplanet)
       # logging.info(targetarrmy)

      #  if len(targetplanet) or turn > 10 == 0:
            AttackOwnerPlanet = True
            ignore_planttacksame = True

        for planet in targetplanet:
            if arrmy.can_dock(planet) and (not planet.is_owned() or planet.owner.id != Map.my_id) and not planet in listofplantdock and turn < 150:
                if AttackOwnerPlanet:
                    listofplantdock.append(planet)
                #logging.info("try do dock1 : " + str(arrmy.id) +
                             "id plan : " + str(planet.id))
                commands.append(arrmy.dock(planet))
                break

            elif (arrmy.can_dock(planet) and planet.is_owned() and planet.owner.id == Map.my_id and not planet.is_full()) and turn < 150:
                commands.append(arrmy.dock(planet))
                #logging.info("try do dock : " + str(arrmy.id) +
                             "id plan : " + str(planet.id))
                break
            else:
                if planet in Planet_has_been_attacked and not ignore_planttacksame:

                    continue
                else:
                    if not planet.is_owned() or planet.owner.id != Map.my_id:
                        if planet.is_owned():
                            xy = arrmy.closest_point_to(
                                planet.all_docked_ships()[0])
                        else:
                            xy = arrmy.closest_point_to(planet)

                        navigate_command = arrmy.navigate(
                            xy,
                            Map,
                            speed=int(7),
                            ignore_ships=False)
                        #logging.info("navigate: " + str(arrmy.id) +
                                     " to :" + str(planet.id))
                    else:
                        continue
                    if navigate_command:
                        commands.append(navigate_command)
                        Planet_has_been_attacked.append(planet)

                        break
    game.send_command_queue(commands)
    # next
# bye
