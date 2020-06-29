import hlt
import logging
game = hlt.Game("Faster one ")
logging.info("Starting my Faster bot!")

while True:
    Map = game.update_map()
    commands = []
    """
    الخطة

    لا يقوم بالهجوم على نفس الكوكب اكثر من مره بنفس الفريم


    قرار احتلال العدو او الكواكب الفارغة يعتمد على عدد الكواكب المحتلة
    في حال كان احتل نسبة تصل 40% من لعبة يقوم بتجميع القوات والتنقل من كوكب الى كوكب للاحتال السريع

    """
    # TODO جلب عدد كل القوات
    # TODO جلب عدد القوات الخاصة بي

    # TODO جلب كل الكواكب
    # TODO جلب الكواكب الخاصة بي

    # TODO نمط الاحتلال الفارغ
    # TODO نمط احتلال العدو
    for arrmy in Map.get_me().all_ships():

        if arrmy.docking_status != arrmy.DockingStatus.UNDOCKED:
            continue

        planetattack = game.map.nearby_entities_by_distance(arrmy)
        Planet_has_been_attacked = []
        logging.info(planetattack)
        for planet in planetattack:
            if planet.is_owned():
                continue

            if arrmy.can_dock(planet):

                    commands.append(arrmy.dock(planet))
            else:
                if planet in Planet_has_been_attacked:
                    continue
                else:

                    navigate_command = arrmy.navigate(
                    arrmy.closest_point_to(planet),
                    Map,
                    speed=int(hlt.constants.MAX_SPEED),
                    ignore_ships=False)

                    if navigate_command:
                        commands.append(navigate_command)
                        Planet_has_been_attacked.append(planet)
                        break

    game.send_command_queue(commands)
    # next
# bye
