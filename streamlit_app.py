
import streamlit as st
from datetime import datetime, timedelta

def calculate_duration(start_time, end_time):
    # Calculate duration considering the case when end_time is past midnight
    if end_time < start_time:
        end_time += timedelta(days=1)
    duration = end_time - start_time
    return duration

def main():
    st.set_page_config(page_title="Shift Duration Calculator", page_icon="⏰", layout="centered")

    st.title("Eshaan's Shift Duration Calculator")
    st.write("Add your shifts and calculate total duration.")

    # Session state to hold shifts
    if 'shifts' not in st.session_state:
        st.session_state['shifts'] = []

    with st.form("Add New Shift"):
        shift_date = st.date_input("Select Shift Date")

        # Time selectors for start and end times including AM/PM
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 🟦 Start Time") 
            start_hour = st.number_input("Start Hour", min_value=1, max_value=12, value=9, key="start_hour")
            start_minute = st.number_input("Start Minute", min_value=0, max_value=59, value=0, key="start_minute")
            start_am_pm = st.selectbox("Start AM/PM", options=["AM", "PM"], key="start_ampm")
        
        with col2:
            st.markdown("### 🟥 End Time")
            end_hour = st.number_input("End Hour", min_value=1, max_value=12, value=5, key="end_hour")
            end_minute = st.number_input("End Minute", min_value=0, max_value=59, value=0, key="end_minute")
            end_am_pm = st.selectbox("End AM/PM", options=["AM", "PM"], key="end_ampm")

        submit = st.form_submit_button("Add Shift")

        if submit:
            # Convert 12-hour to 24-hour for start time
            s_hour = start_hour % 12
            if start_am_pm == "PM":
                s_hour += 12
            s_time = datetime.combine(shift_date, datetime.min.time()).replace(hour=s_hour, minute=start_minute)

            # Convert 12-hour to 24-hour for end time
            e_hour = end_hour % 12
            if end_am_pm == "PM":
                e_hour += 12
            e_time = datetime.combine(shift_date, datetime.min.time()).replace(hour=e_hour, minute=end_minute)

            shift_duration = calculate_duration(s_time, e_time)
            st.session_state.shifts.append({
                'date': shift_date,
                'start': s_time,
                'end': e_time,
                'duration': shift_duration
            })
            st.success(f"Shift added: {shift_date.strftime('%Y-%m-%d')} from {start_hour:02d}:{start_minute:02d} {start_am_pm} to {end_hour:02d}:{end_minute:02d} {end_am_pm} (Duration: {shift_duration})")

    # Show all shifts and total duration
    if st.session_state.shifts:
        st.subheader("Shifts Added:")
        total_duration = timedelta()
        for idx, shift in enumerate(st.session_state.shifts, 1):
            dur = shift['duration']
            total_duration += dur
            hours, remainder = divmod(dur.seconds, 3600)
            minutes = remainder // 60
            st.write(f"{idx}. Date: {shift['date'].strftime('%Y-%m-%d')}, Start: {shift['start'].strftime('%I:%M %p')}, End: {shift['end'].strftime('%I:%M %p')}, Duration: {hours}h {minutes}m")

        # Total duration display
        total_hours = total_duration.seconds // 3600 + total_duration.days * 24
        total_minutes = (total_duration.seconds % 3600) // 60
        st.markdown("---")
        st.header(f"Total Shift Duration: {total_hours} hours and {total_minutes} minutes")

if __name__ == "__main__":
    main()

