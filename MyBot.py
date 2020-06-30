import hlt
import logging
import random
from collections import OrderedDict
game = hlt.Game("Faster -V3")
logging.info("Starting my Faster bot!")
ignore_planttacksame = False
AttackOwnerPlanet = False
turn = 0
while True:
    turn = turn + 1
    Map = game.update_map()
    commands = []
    Planet_has_been_attacked = []
    """
    الخطة

    لا يقوم بالهجوم على نفس الكوكب اكثر من مره بنفس الفريم


    قرار احتلال العدو او الكواكب الفارغة يعتمد على عدد الكواكب المحتلة
    في حال كان احتل نسبة تصل 40% من لعبة يقوم بتجميع القوات والتنقل من كوكب الى كوكب للاحتال السريع

    """
    alltroops = Map.get_me().all_ships()
    listofplantdock = []
    for arrmy in alltroops:

        targetplanet = []
        targetarrmy = []

        if arrmy.docking_status != arrmy.DockingStatus.UNDOCKED:

            continue


        entities_by_distance_all = Map.nearby_entities_by_distance(arrmy)

        entities_by_distance_all = sorted(
            entities_by_distance_all.items(), key=lambda entities_by_distance_allX: entities_by_distance_allX[0], reverse=False)

        for target in entities_by_distance_all:
            if isinstance(target[1][0], hlt.entity.Planet) and (not target[1][0].is_owned() or AttackOwnerPlanet):
                targetplanet.append(target[1][0])

          #  else:
          #      logging.info()

       # logging.info(targetplanet)
       # logging.info(targetarrmy)

        if len(targetplanet) == 0 and turn >100:
            AttackOwnerPlanet = True
            ignore_planttacksame = True
        
        for planet in targetplanet:
            if arrmy.can_dock(planet) and (not planet.is_owned() or planet.owner.id != Map.my_id) and not planet in listofplantdock:
                if AttackOwnerPlanet:
                    listofplantdock.append(planet)
                
                commands.append(arrmy.dock(planet))
                
                break
            else:
                if planet in Planet_has_been_attacked and not ignore_planttacksame:

                    continue
                else:
                    if not planet.is_owned() or planet.owner.id != Map.my_id:
                        xy = arrmy.closest_point_to(planet)
                        if AttackOwnerPlanet : 
                            xy = planet.closest_point_to(arrmy)
                        navigate_command = arrmy.navigate(
                            xy,
                            Map,
                            speed=int(hlt.constants.MAX_SPEED),
                            ignore_ships=False)
                    else:
                        continue
                    if navigate_command:
                        commands.append(navigate_command)
                        Planet_has_been_attacked.append(planet)
                        
                        break
    game.send_command_queue(commands)
    # next
# bye
