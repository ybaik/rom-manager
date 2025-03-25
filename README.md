# rom-manager

## Creating a Windows Symbolic Link for RetroBat

To create a symbolic link for RetroBat on a Windows system, follow these steps:
1. Open Command Prompt as Administrator.
2. Use the `mklink` command to create the symbolic link. For example:
   ```shell
   mklink /D "C:\RetroBat\roms\megadrive" "USB:\roms\megadrive"
   ```
3. Confirm the symbolic link has been created successfully.