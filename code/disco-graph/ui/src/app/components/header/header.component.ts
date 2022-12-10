import { HttpErrorResponse } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MatIconRegistry } from "@angular/material/icon";
import { MatSnackBar, MatSnackBarConfig } from '@angular/material/snack-bar';
import { DomSanitizer } from "@angular/platform-browser";
import { AuthenticationService } from 'src/app/services/authentication.service';
import { UserLoginComponent } from '../user-login/user-login.component';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent implements OnInit {

  snackBarConfig: MatSnackBarConfig = {
    duration: 4000,
  }

  constructor(
    private matIconRegistry: MatIconRegistry,
    private domSanatizer: DomSanitizer,
    private authService: AuthenticationService,
    private _snackBar: MatSnackBar,
    public dialog: MatDialog,
    ) {
    this.matIconRegistry.addSvgIcon(
      "disco_graph",
      this.domSanatizer.bypassSecurityTrustResourceUrl("../../../assets/disco-graph-logo_no-text.svg")
    );
  }

  ngOnInit(): void {
  }

  openLoginDialog(){
    const dialogRef = this.dialog.open(UserLoginComponent);
    
    dialogRef.afterClosed().subscribe(loggedIn => {
      if(loggedIn){
        this.openSnackBar('Logged in successfully.')
      }
    });
  }

  logout(){
    this.authService.logout().subscribe({
      error: (error: HttpErrorResponse) => {
        this.openSnackBar('Log out failed.')
        console.log(error);
      },
      complete: () => {
        this.openSnackBar('Logged out successfully.')
      }
    })
  }

  getLoggedInUser(): string{
    return this.authService.loggedInUser;
  }

  isUserLoggedIn(): boolean{
    return Boolean(this.getLoggedInUser());
  }

  openSnackBar(message: string){
    this._snackBar.open(message, 'Dismiss', this.snackBarConfig);
  }

}
