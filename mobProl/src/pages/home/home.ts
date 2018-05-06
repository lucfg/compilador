import { Component, ViewChild, ElementRef } from '@angular/core';
import { Http } from '@angular/http';
import { NavController, ModalController, LoadingController } from 'ionic-angular';
import { OutputPage } from '../output/output';

@Component({
  selector: 'page-home',
  templateUrl: 'home.html'
})
export class HomePage {
  programName: string;
  programCodeString: string;

  quadruples = [];

  // Interface
  @ViewChild('myInput') myInput: ElementRef;
  keyChar = '{';
  keyChar2 = '}';

  constructor(
        public navCtrl: NavController,
        public modalCtrl: ModalController,
        public loadingCtrl: LoadingController,
        private http: Http,
    ) {
    this.programName = "myProgram"
    this.programCodeString = "main() { print(\"Hello world\"); }";
    //this.programCodeString = "var int a; var decim c; var int d; func int uno(int a, decim b, int c){var int z; a = c + 34;} main(){var decim b; var int f; var decim g; var bool myBool; myBool = 1 == 2; g = 1.0; f = 2; b = f+g*(4+5/2); a = 6;}";
  }

  ionViewDidLoad(){
    this.resizeTextArea();
  }

  /**
   * Tries to compile the program and runs it if successful
   */
  async compileAndRun() {
    if (await this.compile()) {
      this.run();
    }
  }

  /**
   * Sends code to python and receives cuadruples to execute
   * Returns true if successful or false if not.
   */
  async compile() {
    console.log("Compiling code...");
    let loading = this.loadingCtrl.create({
      content: 'Compiling your code...'
    });
    loading.present();

    let data = {
        code: "program " + this.programName + "{ "
            + this.programCodeString.replace(/\n/g, "")
            + " }"
    };

    var response;
    try {
      //response = await this.http.post('http://localhost:8080/compile', data).toPromise();
      response = await this.http.post('http://mobprol.us-3.evennode.com/compile', data).toPromise();
    } catch (err) {
      loading.dismiss();
      console.log("Error while trying to access the server: " + err.message);
      alert("Error: It seems like you're not connected to the internet.");
      return false;
    }

    if (!response) {
      loading.dismiss();
      alert("Unexpected error: Server's response is empty.");
      console.log("Server's response was empty.");
      return false;
    }
    
    console.log("normal response is: ");
    console.log(response);
    //let jsonResponse = JSON.parse(response.json());
    let jsonResponse = response.json();
    console.log("Your json is: ")
    console.log(jsonResponse);

    let errData = jsonResponse.errorData;

    if (errData && errData != "") {
      loading.dismiss();
      console.log("Compilation error: " + errData);
      alert(errData);
      return false;
    }

    let quadData = JSON.parse(jsonResponse.data);
    console.log("Your quadData:");
    console.log(quadData);

    for(var i = 0; i < quadData.length; i++) {
      var obj = quadData[i];
      let tempQuad = [];
  
      tempQuad.push(obj.arg1);
      tempQuad.push(obj.arg2);
      tempQuad.push(obj.arg3);
      tempQuad.push(obj.arg4);

      this.quadruples.push(tempQuad);
    }

    console.log("Received quadruples to execute:");
    console.log(this.quadruples);

    loading.dismiss();
    return true;
  }

  /**
   * Uses quadruples to run commands, showing output on screen
   */
  async run() {
    const modal = this.modalCtrl.create(OutputPage, {programName: this.programName, quadruples: this.quadruples});

    modal.onWillDismiss(() => {
      this.quadruples = [];
    });

    modal.present();
  }

  

  /**
   * Makes sure that all code is visible within the text-area
   */
  resizeTextArea() {
    let minHeight = 20;
    let height = this.myInput.nativeElement.scrollHeight;
    if (height < minHeight) {
      height = minHeight;
    }

    this.myInput.nativeElement.style.height = height + 'px';
  }
}
