import wmi
 
def get_bios_info():
    bios_info = {}
    try:
        c = wmi.WMI()
        for bios in c.Win32_BIOS():
            bios_info['Manufacturer'] = bios.Manufacturer
            bios_info['Version'] = bios.Version
            bios_info['ReleaseDate'] = bios.ReleaseDate
            bios_info['SerialNumber'] = bios.SerialNumber
            bios_info['SMBIOSBIOSVersion'] = bios.SMBIOSBIOSVersion
            bios_info['SMBIOSMajorVersion'] = bios.SMBIOSMajorVersion
            bios_info['SMBIOSMinorVersion'] = bios.SMBIOSMinorVersion
            bios_info['IdentificationCode'] = bios.IdentificationCode
            bios_info['Caption'] = bios.Caption
            bios_info['PrimaryBIOS'] = bios.PrimaryBIOS
            bios_info['Status'] = bios.Status
            bios_info['SoftwareElementID'] = bios.SoftwareElementID
            bios_info['SoftwareElementState'] = bios.SoftwareElementState
            bios_info['TargetOperatingSystem'] = bios.TargetOperatingSystem
            bios_info['Description'] = bios.Description
            bios_info['BuildNumber'] = bios.BuildNumber
            bios_info['InstallableLanguages'] = bios.InstallableLanguages
            bios_info['ListOfLanguages'] = bios.ListOfLanguages
            bios_info['OtherTargetOS'] = bios.OtherTargetOS
            bios_info['CurrentLanguage'] = bios.CurrentLanguage
            bios_info['BiosCharacteristics'] = bios.BiosCharacteristics
            bios_info['CurrentTimeZone'] = bios.CurrentTimeZone
            bios_info['NumberOfProcessors'] = bios.NumberOfProcessors
            bios_info['WakeUpType'] = bios.WakeUpType
            bios_info['BootupState'] = bios.BootupState
            bios_info['PrimaryVideoController'] = bios.PrimaryVideoController
            bios_info['SystemBiosMajorVersion'] = bios.SystemBiosMajorVersion
            bios_info['SystemBiosMinorVersion'] = bios.SystemBiosMinorVersion
            bios_info['SystemBiosReleaseDate'] = bios.SystemBiosReleaseDate
    except Exception as e:
        print("Error:", e)
    return bios_info
 
if __name__ == "__main__":
    bios_info = get_bios_info()
    for key, value in bios_info.items():
        print(key + ": " + str(value))
 