import streamlit as st
import pandas as pd
import numpy as np

# Function to calculate BMI
def calculate_bmi(weight, height):
    height_m = height / 100  # Convert height to meters
    return round(weight / (height_m ** 2), 2)

# Function to calculate daily caloric needs
def calculate_caloric_needs(weight, height, age, gender, activity_level, goal):
    if gender == "Male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    activity_multiplier = {
        "Sedentary (little to no exercise)": 1.2,
        "Lightly active (light exercise 1-3 days/week)": 1.375,
        "Moderately active (moderate exercise 3-5 days/week)": 1.55,
        "Very active (hard exercise 6-7 days/week)": 1.725
    }

    daily_calories = bmr * activity_multiplier[activity_level]

    # Adjust based on goal
    if goal == "Lose Weight":
        daily_calories -= 500  # Reduce 500 kcal/day for weight loss
    elif goal == "Gain Muscle":
        daily_calories += 500  # Increase 500 kcal/day for muscle gain

    return round(daily_calories, 2)

# Function to generate a meal plan
def generate_meal_plan(calories):
    meal_plan = {
        "Breakfast": f"Oatmeal with banana and almonds - {round(calories * 0.3)} kcal",
        "Lunch": f"Grilled chicken with quinoa and vegetables - {round(calories * 0.4)} kcal",
        "Dinner": f"Grilled salmon with quinoa and veggies - {round(calories * 0.3)} kcal"
    }
    return meal_plan

# Function to suggest a workout plan
def workout_plan(activity_level):
    workouts = {
        "Sedentary (little to no exercise)": "Light stretching & walking for 30 mins.",
        "Light Activity (light exercise 1-3 days/week)": "30 mins cardio (brisk walking, cycling) + bodyweight exercises.",
        "Moderate Activity (moderate exercise 3-5 days/week)": "Strength training 3 days/week + 30 mins cardio.",
        "High Activity (hard exercise 6-7 days/week)": "60 mins strength training + 30 mins cardio.",
        "Athlete Level (intense daily training)": "Strength + HIIT + Endurance training."
    }
    return workouts.get(activity_level, "Moderate exercise with a balanced routine.")

# Streamlit UI
def main():
    st.title("🏋️‍♂️ Personalized Fitness & Diet Planner")
    st.sidebar.header("User Information")

    # User inputs
    gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
    age = st.sidebar.slider("Age", 15, 80, 25)
    weight = st.sidebar.number_input("Weight (kg)", min_value=30, max_value=150, value=70)
    height = st.sidebar.number_input("Height (cm)", min_value=130, max_value=220, value=170)
    activity_level = st.sidebar.selectbox("Activity Level",
        ["Sedentary (little to no exercise)", "Light Activity (light exercise 1-3 days/week)",
         "Moderate Activity (moderate exercise 3-5 days/week)",
         "Very active (hard exercise 6-7 days/week)",
         "Athlete Level (intense daily training)"])
    goal = st.sidebar.radio("Your Goal", ["Maintain Weight", "Lose Weight", "Gain Muscle"])

    # Calculate BMI
    bmi = calculate_bmi(weight, height)
    st.subheader("Your BMI")
    st.write(f"Your BMI is: **{bmi:.2f}**")

    # Calculate caloric needs
    calories_needed = calculate_bmi(weight, height, age, gender, activity_level, goal)
    st.subheader("Daily Caloric Needs")
    st.write(f"You need approximately **{calories_needed} kcal** per day to achieve your goal.")

    # Generate meal plan
    meal_plan = generate_meal_plan(calories_needed)
    st.subheader("Recommended Meal Plan")
    for meal, details in meal_plan.items():
        st.write(f"**{meal}:** {details}")

    # Recommend workout plan
    st.subheader("Recommended Workout Plan")
    workout_plan_text = workout_plan(activity_level)
    st.write(workout_plan_text)

if __name__ == "__main__":
    import streamlit as st
    main()
