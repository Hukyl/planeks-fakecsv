$("input[type=text]").on('focusout', (element) => {
    element.target.value = element.target.value.trim();
});


function deleteColumn(event) {
    const order = parseInt($(this).parent().find('[data-name=order]').val());
    $(this).parent().parent().parent().parent().remove();
    for (let element of $('div.scheme-column').slice(0, -1)) {
        let elementOrderField = $(element).find('input[data-name=order]');
        if (parseInt(elementOrderField.val()) > order)
            elementOrderField.val(elementOrderField.val() - 1);
    }    
}

$('button#add-column').click(function(event) {
    let originalElement = $('div#add-column-fields');
    const data = [
        {selector: '[data-name=name]', default: ''},
        {selector: '[data-name=type]', default: '-'},
        {selector: '[data-name=order]', default: ''}
    ];
    // -1 beacuse there is add column with `scheme-column` class
    const column_count = $('div.scheme-column').length - 1;
    let element = originalElement.clone();
    element.removeAttr('id');
    for (const fieldData of data) {
        let [label, field] = jQuery.map(element.find(fieldData.selector), i => $(i));
        const key = label.attr('data-name');
        if (field.val() == fieldData.default) {
            alert('Fill all fields before adding column!');
            return;
        }
        field.attr('name', `${column_count}__${key}`);
        label.attr('for', `${column_count}__${key}`);
        let [originalLabel, originalField] = jQuery.map(
            originalElement.find(fieldData.selector), 
            i => $(i)
        );
        field.val(originalField.val());
        originalField.val(fieldData.default);
    }
    element.removeClass('border');
    element.find('button#add-column').remove();
    element.find('button[data-usage=delete-column]').on('click', deleteColumn);
    element.insertBefore(originalElement);
    originalElement.find('[data-name=name]').focus();
});


$('form#main').submit(event => {
    for (let column_name_input of $('input[data-name=name]').slice(0, -1)) {
        if (column_name_input.value === '') {
            alert('All column names should be not null!');
            event.preventDefault(); event.stopPropagation();
        }
    }
    const orders = jQuery.map(
        $('input[data-name=order]'), 
        e => parseInt(e.val())
    ).sort((a, b) => a - b);
    for (let i = 0; i < orders.length; i++) {
        if (orders[i] !== i) {
            alert('Order should start from 0 and be consistent!');
            event.preventDefault(); event.stopPropagation();
        }
    }
    return true;
});