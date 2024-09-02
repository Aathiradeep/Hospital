document.addEventListener('DOMContentLoaded', function() {
    var patientSelect = document.getElementById('patient_id');
    var doctorSelect = document.getElementById('doctor_id');
    var consultationFeeInput = document.getElementById('consultation_fee');
    var patientPhoneInput = document.getElementById('patient_phone');
    var patientAddressInput = document.getElementById('patient_address');

    // Function to update consultation fee
    function updateConsultationFee() {
        var selectedOption = doctorSelect.options[doctorSelect.selectedIndex];
        var fee = selectedOption.getAttribute('data-fee');
        consultationFeeInput.value = fee ? parseFloat(fee).toFixed(2) : '';
    }

    // Function to update patient details
    function updatePatientDetails() {
        var patientId = patientSelect.value;

        if (patientId) {
            // Fetch patient details using AJAX
            fetch(`/billing/get_patient_details/${patientId}/`)
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        console.error(data.error);
                        return;
                    }
                    // Set the patient details
                    patientPhoneInput.value = data.phone_number || '';
                    patientAddressInput.value = data.address || '';
                })
                .catch(error => console.error('Error fetching patient details:', error));
        } else {
            // Clear fields if no patient is selected
            patientPhoneInput.value = '';
            patientAddressInput.value = '';
        }
    }

    // Update consultation fee on page load if doctor is already selected
    updateConsultationFee();

    // Update consultation fee when doctor changes
    doctorSelect.addEventListener('change', updateConsultationFee);

    // Update patient details when patient changes
    patientSelect.addEventListener('change', updatePatientDetails);
});
