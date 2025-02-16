# Torque Calculation for Each Motor in the Robotic Arm

## Problem Overview
This document explains the method for calculating the required torque for each motor in a robotic arm designed to lift a 1 kg weight at various segments. Each motor controls a specific segment of the arm, and the torque required depends on the arm segment's length and the force due to the weight being lifted.

---

### Motor 1 (Base Motor - Large Segment)

**Parameters:**
- Arm length:  
  **r₁ = 15 cm = 0.15 m**
- Weight to lift:  
  **m = 1 kg**
- Force (F):  
  **F = m × g = 1 × 9.81 = 9.81 N**

**Calculation:**
- Torque:  
  **τ₁ = F × r₁ = 9.81 × 0.15 = 1.47 Nm**

**Result:**  
The required torque for **Motor 1** is **1.47 Nm**.

---

### Motor 2 (Second Motor - Medium Segment)

**Parameters:**
- Arm length:  
  **r₂ = 10 cm = 0.1 m**
- Weight to lift:  
  **m = 1 kg**
- Force (F):  
  **F = 9.81 N**

**Calculation:**
- Torque:  
  **τ₂ = F × r₂ = 9.81 × 0.1 = 0.981 Nm**

**Result:**  
The required torque for **Motor 2** is **0.981 Nm**.

---

### Motor 3 (Third Motor - Small Segment)

**Parameters:**
- Arm length:  
  **r₃ = 4 cm = 0.04 m**
- Weight to lift:  
  **m = 1 kg**
- Force (F):  
  **F = 9.81 N**

**Calculation:**
- Torque:  
  **τ₃ = F × r₃ = 9.81 × 0.04 = 0.3924 Nm**

**Result:**  
The required torque for **Motor 3** is **0.3924 Nm**.

---

## Conclusion
- **Motor 1** needs **1.47 Nm** of torque.  
- **Motor 2** requires **0.981 Nm** of torque.  
- **Motor 3** requires **0.3924 Nm** of torque.
