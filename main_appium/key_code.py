import os
class InputMethod:
    def enable_samsung_ime(self, device_name):
        os.system(f"adb -s {device_name} shell ime set com.samsung.android.svoiceime/.SamsungVoiceReco")
