int main() {

    char c = 'a';

    switch (c) {
        case 'a':
        case 'b':
            break;
        default:
            break;
    }

    while (c == 'a') {
        c = 'b';
    }

    return 0;
}