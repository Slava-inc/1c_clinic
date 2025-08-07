# bot/services/mis_service.py
import aiohttp

class MISService:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key

    async def get_doctors_schedule(self, doctor_id: int):
        url = f"{self.base_url}/doctors/{doctor_id}/schedule"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                return await response.json()

    async def create_appointment(self, patient_id: int, doctor_id: int, appointment_date: str):
        url = f"{self.base_url}/appointments"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {"patient_id": patient_id, "doctor_id": doctor_id, "appointment_date": appointment_date}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as response:
                return await response.json()