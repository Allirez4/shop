// This ensures the script runs after the entire page is loaded.
document.addEventListener("DOMContentLoaded", function() {
    // Django admin uses its own version of jQuery.
    // We use this function to safely use the '$' shortcut for jQuery.
    (function($){
        $(document).ready(function(){
            // Select the category and subcategory dropdowns by their ID.
            const categorySelect = $('#id_category');
            const subcategorySelect = $('#id_subcategory');
            const subcategoriesUrl = '/get-subcategories/'; 
            // This function is triggered whenever the user changes the category dropdown.
            categorySelect.change(function(){
                const categoryId = $(this).val(); // Get the ID of the selected category.

                if (categoryId) {
                    // If a category is selected, make an AJAX request to our Django view.
                    $.ajax({
                        url: subcategoriesUrl,
                        data: {
                            'category_id': categoryId
                        },
                        dataType: 'json',
                        success: function(data){
                            // This code runs when we successfully get a response from the server.
                            subcategorySelect.empty(); // Clear all existing options.
                            
                            // Add a default, empty option.
                            subcategorySelect.append($('<option>', {
                                value: '',
                                text: '---------'
                            }));

                            // Loop through the data (our subcategories) and add them as new options.
                            $.each(data, function(key, value){
                                subcategorySelect.append($('<option>', {
                                    value: key,   // The subcategory ID
                                    text: value   // The subcategory name
                                }));
                            });
                        }
                    });
                } else {
                    // If no category is selected (e.g., the user chooses the '---' option),
                    // clear the subcategory dropdown.
                    subcategorySelect.empty();
                }
            });
        });
    })(django.jQuery);
});