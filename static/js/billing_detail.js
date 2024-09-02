// static/js/billing_detail.js
document.addEventListener('DOMContentLoaded', function() {
    var billSelect = document.getElementById('bill_id');
    var billDetailsDiv = document.getElementById('bill-details');

    billSelect.addEventListener('change', function() {
        var billId = billSelect.value;

        if (billId) {
            // Fetch bill details using AJAX
            fetch(`/billing/get_bill_details/${billId}/`)
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        console.error(data.error);
                        return;
                    }

                    // Display the bill details
                    billDetailsDiv.innerHTML = `
                        <h2>Bill Details for ${data.id}</h2>
                        <p><strong>Doctor:</strong> Dr. ${data.doctor}</p>
                        <p><strong>Date Generated:</strong> ${data.date_generated}</p>
                        <p><strong>Amount:</strong> $${data.amount}</p>
                        <p><strong>Patient Phone:</strong> ${data.patient_phone}</p>
                        <p><strong>Patient Address:</strong> ${data.patient_address}</p>
                        <p><strong>Room Charge:</strong> $${data.room_charge}</p>
                        <p><strong>Medicine Cost:</strong> $${data.medicine_cost}</p>
                        <p><strong>Other Charges:</strong> $${data.other_charges}</p>
                        <p><strong>Days Stayed:</strong> ${data.days_stayed}</p>
                        <p><strong>Consultation Fee:</strong> $${data.consultation_fee}</p>
                        <div class="buttons-box">
                            <a href="/billing/download_pdf/${data.id}/" class="btn btn-primary">Download Bill</a>
                        </div>
                    `;
                })
                .catch(error => console.error('Error fetching bill details:', error));
        } else {
            // Clear the bill details if no bill is selected
            billDetailsDiv.innerHTML = '<p>Select a bill from the dropdown to view details.</p>';
        }
    });
});
