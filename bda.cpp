#include <stdio.h>
#include <stdint.h>
 
// Structure to represent BIOS Data Area (BDA)
struct BDAData {
    uint16_t comPorts[4];       // IO ports for COM1-COM4 serial
    uint16_t parallelPorts[3];  // IO ports for LPT1-LPT3 parallel
    uint16_t ebdaBaseAddress;   // EBDA base address
    uint8_t  packedFlags;       // Packed bit flags for detected hardware
    uint16_t unusedMemoryKB;    // Number of kilobytes before EBDA / unusable memory
    uint16_t keyboardFlags;     // Keyboard state flags
    // Add more fields as needed
};
 
// Function to read BIOS Data Area (BDA)
void readBDA(struct BDAData* bda) {
    // Read BDA data from memory addresses
    memcpy(bda, (void*)0x0400, sizeof(struct BDAData));
}
 
int main() {
    // Create a structure to hold BDA data
    struct BDAData bdaData;
 
    // Read BDA data
    readBDA(&bdaData);
 
    // Print BDA information
    printf("EBDA Base Address: 0x%X\n", bdaData.ebdaBaseAddress);
    printf("IO Ports for COM1-COM4: ");
    for (int i = 0; i < 4; i++) {
        printf("0x%X ", bdaData.comPorts[i]);
    }
    printf("\nIO Ports for LPT1-LPT3: ");
    for (int i = 0; i < 3; i++) {
        printf("0x%X ", bdaData.parallelPorts[i]);
    }
    printf("\n");
    // Print more BDA information as needed
 
    return 0;
}