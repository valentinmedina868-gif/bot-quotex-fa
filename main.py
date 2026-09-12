import asyncio
import logging
from datetime import datetime
import pandas as pd
import pytz
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup

# ========= CONFIGURACIÓN Y DATOS PERSONALES =========
TOKEN_BOT = "8846323720:AAG5AhffH8hF3iW1jyjzGkBfZOoYwgj7-LE"

# Canales reales (Ambos privados por ID numérico)
GRUPO_VIP = "-1003850366869"
GRUPO_GRATIS = "-1003056096786"

# Datos de Afiliado y Soporte
PROPIETARIO = "@fmedina19"
LINK_BROKER = "https://broker-qx.pro/?lid=2058184"

bot = Bot(token=TOKEN_BOT)

# Contador de resultados del canal Gratuito
contador_gratis = {"WIN": 0, "LOSS": 0}

# ========= BOTÓN ANCHO INTERACTIVO DE PIE =========
def obtener_botones_pie():
    """Genera los botones anchos interactivos al pie del mensaje."""
    keyboard = [
        [InlineKeyboardButton("📲 Crear Cuenta Oficial en Quotex", url=LINK_BROKER)],
        [InlineKeyboardButton("📩 Unirse al VIP / Consultas", url=f"https://t.me/fmedina19")]
    ]
    return InlineKeyboardMarkup(keyboard)

# ========= REVISIÓN DE HORARIOS =========
def es_horario_gratuito():
    """Bloques autorizados para enviar señales al canal Gratuito (Hora Argentina)"""
    tz_ba = pytz.timezone('America/Argentina/Buenos_Aires')
    hora = datetime.now(tz_ba).hour
    return (8 <= hora < 9) or (12 <= hora < 13) or (18 <= hora < 19) or (23 <= hora < 24)

# ========= PLANTILLAS DE SEÑAL DE ENTRADA Y RESULTADO =========
def crear_plantilla_entrada(par, hora_entrada, direccion):
    tz_ba = pytz.timezone('America/Argentina/Buenos_Aires')
    fmt = "%H:%M"
    
    t_entrada = datetime.strptime(hora_entrada, fmt)
    t_termina = t_entrada + pd.Timedelta(minutes=1)
    t_proteccion = t_entrada + pd.Timedelta(minutes=2)
    
    emoji_dir = "ARRIBA 🟢" if direccion == "ARRIBA" else "ABAJO 🔴"
    
    return (
        f"🎓 **FA ACADEMY | BINARIAS VIP** 🎓\n"
        f"💲 **OPORTUNIDAD ENCONTRADA** 💲\n\n"
        f"⏱️ 1 minuto de operación\n"
        f"📊 `{par}` {hora_entrada} {emoji_dir}\n"
        f"🌐 Zona horaria: (UTC-3)\n"
        f"⏳ Termina a las: {t_termina.strftime(fmt)}\n"
        f"🛡️ 1ª PROTECCIÓN Termina a las {t_proteccion.strftime(fmt)}\n"
        f"👉 [Haga clic para abrir el corredor]({LINK_BROKER})\n\n"
        f"❓ ¿Aún no sabes operar? {PROPIETARIO}\n"
        f"📈 FINANZAS EN ASCENSO\n"
        f"⚠️ No operar si el payout está por debajo del 80%\n"
        f"⚠️ No operar contra tendencia\n"
        f"⚠️ Evitar velas Dojis"
    )

def crear_plantilla_resultado(par, resultado_tipo):
    if resultado_tipo == "WIN":
        return f"✅ `{par}` GANADA DIRECTA 🟩"
    elif resultado_tipo == "MTG":
        return f"🔄 `{par}` GANADA EN 1ª PROTECCIÓN 🟨"
    else:
        return f"❌ `{par}` LOSS 🟥"

# ========= ANUNCIOS Y PROMOCIONES (CANAL GRATUITO) =========
async def enviar_saludo_diario(bot_instancia):
    tz_ba = pytz.timezone('America/Argentina/Buenos_Aires')
    dias_semana = {
        0: "Lunes 🚀 ¡A arrancar la semana con toda la fuerza!",
        1: "Martes 💪 ¡Mantenemos el enfoque y la disciplina!",
        2: "Miércoles ⚡ ¡Mitad de semana, a consolidar ganancias!",
        3: "Jueves 🔥 ¡Preparamos el terreno para cerrar en positivo!",
        4: "Viernes 🎉 ¡Último esfuerzo de la semana laboral!",
        5: "Sábado 📈 ¡Aprovechando el mercado OTC al máximo!",
        6: "Domingo 🛡️ ¡Planificando el éxito de la semana que entra!"
    }
    
    dia_num = datetime.now(tz_ba).weekday()
    frase_dia = dias_semana.get(dia_num, "¡Un excelente día para operar!")
    
    mensaje = (
        f"☀️ **¡BUENOS DÍAS A TODOS!** ☀️\n\n"
        f"📅 Hoy es: **{frase_dia}**\n\n"
        f"Recordá operar siempre con gestión de riesgo y mantener la calma.\n"
        f"📲 Creá tu cuenta oficial en Quotex aquí: [Registrarse en Quotex]({LINK_BROKER})\n\n"
        f"📩 Consultas VIP y soporte: {PROPIETARIO}\n\n"
        f"🔥 *¡Atentos a las señales del día!*"
    )
    
    await bot_instancia.send_message(
        chat_id=GRUPO_GRATIS, 
        text=mensaje, 
        parse_mode='Markdown', 
        disable_web_page_preview=True,
        reply_markup=obtener_botones_pie()
    )

async def enviar_alerta_previa_sesion(bot_instancia, bloque_nombre):
    mensaje = (
        f"🔔 **¡ATENCIÓN COMUNIDAD!** 🔔\n\n"
        f"⏰ En **20 minutos** iniciamos la sesión de señales de la **{bloque_nombre}**.\n\n"
        f"🧠 **REGLAS DE ORO Y GESTIÓN EMOCIONAL:**\n"
        f"▪️ **No sobreoperes:** Si ya alcanzaste tu meta de ganancias del día (Take Profit), ¡retírate y disfruta tu día!\n"
        f"▪️ **Esto no es un juego:** El trading se domina con disciplina, estudio y cabeza fría, no con emociones ni avaricia.\n"
        f"▪️ Respetá tu Stop Loss y mantené un Payout mínimo del 80%.\n\n"
        f"📩 ¿Tenés dudas o querés aprender a operar con nuestra estrategia? Escribime directo a: {PROPIETARIO}\n\n"
        f"🚀 *¡Preparen sus plataformas con responsabilidad!*"
    )
    
    await bot_instancia.send_message(
        chat_id=GRUPO_GRATIS, 
        text=mensaje, 
        parse_mode='Markdown', 
        disable_web_page_preview=True,
        reply_markup=obtener_botones_pie()
    )

async def enviar_promocion_academia_vip(bot_instancia):
    mensaje_promo = (
        f"🚀 **¿QUERÉS APRENDER A OPERAR EN SERIO Y CAMBIAR TUS RESULTADOS?** 🚀\n\n"
        f"🎓 **ACADEMIA FINANZAS EN ASCENSO** 🎓\n"
        f"Te invitamos a formar parte de nuestra academia de trading para llevarte de cero a profesional:\n\n"
        f"📚 Libros y PDF educativos de alto valor.\n"
        f"🎥 Librería de clases grabadas para estudiar a tu ritmo.\n"
        f"📈 Sesiones y clases de análisis técnico en vivo.\n"
        f"🧠 Estrategias avanzadas y gestión de riesgo profesional.\n\n"
        f"💡 *Inversión en la Academia:* **150 USD** (Acceso completo).\n\n"
        f"─────────────────────────────\n"
        f"💎 **¿PREFERÍS MÁS SEÑALES Y OPERAR 24/7?** 💎\n"
        f"Sumate a nuestro **CANAL VIP 100% GRATUITO**.\n\n"
        f"📌 **Requisitos para ingresar al VIP Gratis:**\n"
        f"1️⃣ Creá tu cuenta oficial en Quotex desde este enlace: [Crear Cuenta en Quotex]({LINK_BROKER})\n"
        f"2️⃣ Realizá un depósito mínimo de **50 USD** para operar tu propia cuenta.\n"
        f"3️⃣ Enviale tu ID de cuenta a {PROPIETARIO} para verificar y darte acceso inmediato.\n\n"
        f"📲 **¿Dudas o inscripciones? Escribinos directo a:** {PROPIETARIO}"
    )

    await bot_instancia.send_message(
        chat_id=GRUPO_GRATIS, 
        text=mensaje_promo, 
        parse_mode='Markdown', 
        disable_web_page_preview=True,
        reply_markup=obtener_botones_pie()
    )

async def enviar_resumen_cierre(bot_instancia):
    global contador_gratis
    wins = contador_gratis["WIN"]
    losses = contador_gratis["LOSS"]
    
    total_ops = wins + losses
    efectividad = 95.0 if total_ops > 0 and (wins/total_ops) >= 0.95 else (round((wins / total_ops) * 100, 1) if total_ops > 0 else 0)
    
    mensaje = (
        f"📊 **RESUMEN DIARIO DE RESULTADOS** 📊\n"
        f"___________________________________\n\n"
        f"✅ Operaciones Ganadas (WIN): **{wins}**\n"
        f"❌ Operaciones Perdidas (LOSS): **{losses}**\n"
        f"📈 Efectividad del día: **{efectividad}%**\n"
        f"___________________________________\n\n"
        f"💡 **Recordatorio importante:** El mercado premia a los pacientes y castiga a los desesperados. Si hoy tuviste una sesión positiva, cuidá tu capital. Si no se dio, respetá tu Stop Loss y volvé mañana.\n\n"
        f"💎 ¿Querés señales las 24 hs en el VIP o estudiar en la Academia Finanzas en Ascenso? Escribime a: {PROPIETARIO}\n\n"
        f"🌙 ¡Nos vemos mañana con más análisis profesional!"
    )
    
    await bot_instancia.send_message(
        chat_id=GRUPO_GRATIS, 
        text=mensaje, 
        parse_mode='Markdown', 
        disable_web_page_preview=True,
        reply_markup=obtener_botones_pie()
    )
    
    contador_gratis["WIN"] = 0
    contador_gratis["LOSS"] = 0

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

if __name__ == "__main__":
    asyncio.run(main())
