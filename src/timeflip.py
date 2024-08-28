import asyncio
import threading
from bleak import BleakError
from pytimefliplib.async_client import AsyncClient, TimeFlipRuntimeError
from config import DEVICE_MAC, DEVICE_PASSWORD
from toggl import send_tasks_to_toggl
from datetime import datetime, timezone

async def timeflip_main(saved_facet_values, gui_logger):
    last_facet = None
    detect_facet_count = 0
     # Log the saved facet values for debugging
    gui_logger.debug(f"Saved facet values at start: {saved_facet_values}")

    try:
        async with AsyncClient(DEVICE_MAC) as client:
            gui_logger.debug('Connected')
            while True:
                await client.setup(DEVICE_PASSWORD)
                current_facet = await client.current_facet()

                # Ensure current_facet is in saved_facet_values
                if f"Facet {current_facet}" in saved_facet_values:
                    log_message = f'Current facet: {current_facet} - {saved_facet_values[f"Facet {current_facet}"]}'
                    gui_logger.debug(log_message)

                    if last_facet is None:
                        last_facet = current_facet

                    if current_facet == last_facet:
                        detect_facet_count += 1
                    else:
                        last_facet = current_facet
                        detect_facet_count = 1

                    if detect_facet_count == 5:
                        description = saved_facet_values[f"Facet {last_facet}"]
                        start_time = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
                        send_tasks_to_toggl(description, start_time, gui_logger)
                        detect_facet_count = 0
                else:
                    gui_logger.warning(f"Facet {current_facet} not found in saved facet values.")

                await asyncio.sleep(1)
    except TimeFlipRuntimeError as e:
        gui_logger.error(f"TimeFlip runtime error: {e}")
    except BleakError as e:
        gui_logger.error(f"Bluetooth error: {e}")
    except Exception as e:
        gui_logger.error(f"Error: {e}")

def start_timeflip_thread(saved_facet_values, gui_logger):
    
    def run_timeflip():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(timeflip_main(saved_facet_values, gui_logger))
        loop.close()

    thread = threading.Thread(target=run_timeflip)
    thread.daemon = True
    thread.start()