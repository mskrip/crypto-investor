function  makeToasts(array) {
    if (array !== undefined) {
        for (var i = 0; i < array.length; i++) {
            M.toast({
                html: array[i].message,
                displayLength: 3000,
                classes: array[i].color + ' rounded pulse'
            });
        }
    }
}
