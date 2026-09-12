# ========= RELOJ DE PROGRAMACIÓN Y BUCLE PRINCIPAL =========
async def reloj_tareas_programadas(bot_instancia):
    tz_ba = pytz.timezone('America/Argentina/Buenos_Aires')
    ejecutado = {k: False for k in ["06:00", "07:40", "10:00", "11:40", "15:00", "17:40", "20:00", "22:40", "23:59"]}

    while True:
        try:
            ahora = datetime.now(tz_ba)
            hm = ahora.strftime("%H:%M")

            if hm == "06:00" and not ejecutado["06:00"]:
                await enviar_saludo_diario(bot_instancia)
                ejecutado["06:00"] = True
            elif hm == "07:40" and not ejecutado["07:40"]:
                await enviar_alerta_previa_sesion(bot_instancia, "Mañana (08:00 hs)")
                ejecutado["07:40"] = True
            elif hm == "10:00" and not ejecutado["10:00"]:
                await enviar_promocion_academia_vip(bot_instancia)
                ejecutado["10:00"] = True
            elif hm == "11:40" and not ejecutado["11:40"]:
                await enviar_alerta_previa_sesion(bot_instancia, "Mediodía (12:00 hs)")
                ejecutado["11:40"] = True
            elif hm == "15:00" and not ejecutado["15:00"]:
                await enviar_promocion_academia_vip(bot_instancia)
                ejecutado["15:00"] = True
            elif hm == "17:40" and not ejecutado["17:40"]:
                await enviar_alerta_previa_sesion(bot_instancia, "Tarde (18:00 hs)")
                ejecutado["17:40"] = True
            elif hm == "20:00" and not ejecutado["20:00"]:
                await enviar_promocion_academia_vip(bot_instancia)
                ejecutado["20:00"] = True
            elif hm == "22:40" and not ejecutado["22:40"]:
                await enviar_alerta_previa_sesion(bot_instancia, "Noche (23:00 hs)")
                ejecutado["22:40"] = True
            elif hm == "23:59" and not ejecutado["23:59"]:
                await enviar_resumen_cierre(bot_instancia)
                ejecutado["23:59"] = True

            for clave in ejecutado:
                if hm != clave:
                    ejecutado[clave] = False
        except Exception as e:
            logging.error(f"Error en reloj: {e}")

        await asyncio.sleep(20)

async def bucle_analizador_senales():
    """Bucle dedicado a escanear velas y enviar señales al VIP 24/7"""
    while True:
        try:
            # Aquí corre la lógica del escáner de velas
            pass
        except Exception as e:
            logging.error(f"Error en escáner: {e}")
        await asyncio.sleep(360)

async def main():
    print("Iniciando Bot de Quotex FA ACADEMY en Render...")
    tarea_senales = asyncio.create_task(bucle_analizador_senales())
    tarea_reloj = asyncio.create_task(reloj_tareas_programadas(bot))
    await asyncio.gather(tarea_senales, tarea_reloj)

if name == "main":
    asyncio.run(main())
