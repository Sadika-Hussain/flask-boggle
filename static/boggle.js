class BoggleGame {
    constructor() {
        // Cache DOM elements
        this.$guess = $('#guess');
        this.$submit = $('#submit');
        this.$resDiv = $('#response');
        this.$resMsg = $('#res-msg')
        this.$currentScore = $('#score');
        this.$timer = $('#timer');
        this.$restart = $('#restart');
        this.$highScore = $('#highscore');
        this.$plays = $('#plays');
        
        // Initialize game variables
        this.highScore = 0;
        this.plays = 0;
        this.currentScore = 0;
        this.guessedWords = new Set();
        this.timeLeft = 60;

        // Bind event listeners
        this.$submit.on('click', (evt) => this.handleGuess(evt));
        this.$restart.on('click', () => this.restartGame());
        $(document).ready(() => this.startTimer());
    }

    // Function to handle guess submission 
    async handleGuess(evt) {
        evt.preventDefault();
        const guessVal = this.$guess.val().trim(); 

        // Do nothing if the input is empty
        if (!guessVal) {
            return;
        }

        // Check if the word has already been guessed
        if (this.guessedWords.has(guessVal)) {
            this.$resMsg.text(`${guessVal} was already found.`);
            this.$resDiv.addClass('result-not-valid').removeClass('result-ok');
            this.$resDiv.show();
            this.$guess.val(''); // Clear the input
            return;
        }

        try {
            // Make a POST request to submit the guess
            const response = await axios.post('/submit', { guess: guessVal });

            const res = response.data.result;
            this.$resDiv.show(); // Show the result message

            if (res === 'ok') {
                // If guess is valid, update the score and guessed words set
                this.$resMsg.text(`${guessVal} is on the board!`);
                this.$resDiv.addClass('result-ok').removeClass('result-not-valid');
                this.currentScore += guessVal.length; // Add word length to score
                this.updateScore(); // Update score display
                this.guessedWords.add(guessVal); // Add word to guessed set
            } else if (res === 'not-word') {
                this.$resMsg.text(`${guessVal} is not a valid word.`);
                this.$resDiv.addClass('result-not-valid').removeClass('result-ok');
            } else {
                this.$resMsg.text(`${guessVal} is not on the board.`);
                this.$resDiv.addClass('result-not-valid').removeClass('result-ok');
            }
        } catch (error) {
            // Handle any errors from the request
            console.error('Error:', error);
            this.$resDiv.text('Error: ' + error.message);
        }

        this.$guess.val(''); // Clear the input field after submission
    }

    updateScore() {
        this.$currentScore.text(`Current Score: ${this.currentScore}`);
       
        this.$currentScore.show(); // Ensure the score element is visible
        
    }

    // Start the game timer
    startTimer() {
        this.updateScore(); // Initialize score display

        // Set up a 1-second interval for the timer
        const timer = setInterval(() => {
            this.$timer.text(`Time left: ${this.timeLeft} seconds`);
            this.timeLeft--; // Decrease the time left

            // When time runs out, stop the timer and disable input
            if (this.timeLeft < 0) {
                clearInterval(timer); // Stop the timer
                this.$guess.prop('disabled', true); // Disable the input
                this.$submit.prop('disabled', true); // Disable the submit button
                this.saveData(); // Save the game score
                this.$restart.show(); // Show game restart button
            }
        }, 1000); // Update every second
    }

    // Save the game data to the server
    async saveData() {
        try {
            // Send the current score to the server
            const response = await axios.post('/complete', { score: this.currentScore });
            const data = response.data;
            this.highScore = data.highScore;
            this.plays = data.playCount;
            this.updateScore();
        } catch (error) {
            // Handle any errors from the request
            console.error('Error:', error);
            this.$res.text('Error: ' + error.message);
        }
    }
    
    restartGame() {
        window.location.href = '/';
    }
}

// Initialize a new game instance
const game = new BoggleGame();



