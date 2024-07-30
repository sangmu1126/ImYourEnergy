document.addEventListener('DOMContentLoaded', (event) => {
    // Event listeners for buttons to open modals
    document.getElementById('nicknameChangeBtn').onclick = function() {
        openModal('nicknameChangeModal');
    };

    document.getElementById('passwordChangeBtn').onclick = function() {
        openModal('passwordChangeModal');
    };

    document.getElementById('withdrawalBtn').onclick = function() {
        openModal('withdrawalModal');
    };

    document.getElementById('logoutBtn').onclick = function() {
        openModal('logoutModal');
    };

    // Function to open modal
    function openModal(modalId) {
        document.getElementById(modalId).style.display = "block";
    }

    // Function to close modal
    function closeModal(modalId) {
        document.getElementById(modalId).style.display = "none";
    }

    // Event listener to close modals when clicking on the close button
    document.querySelectorAll('.close').forEach(function(element) {
        element.onclick = function() {
            closeModal(element.closest('.modal').id);
        };
    });

    // Close the modal when clicking outside of the modal
    window.onclick = function(event) {
        if (event.target.classList.contains('modal')) {
            event.target.style.display = "none";
        }
    };

    // Handle the post-withdrawal modal display
    document.querySelector('#confirmWithdrawalBtn').onclick = function() {
        closeModal('withdrawalModal');
        openModal('postWithdrawalModal');
    };
});
