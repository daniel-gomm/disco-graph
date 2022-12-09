import { Component, OnInit } from '@angular/core';
import { MatIconRegistry } from "@angular/material/icon";
import { DomSanitizer } from "@angular/platform-browser";

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent implements OnInit {

  constructor(
    private matIconRegistry: MatIconRegistry,
    private domSanatizer: DomSanitizer
    ) { 
    this.matIconRegistry.addSvgIcon(
      "sci_graph",
      this.domSanatizer.bypassSecurityTrustResourceUrl("../../../assets/sci-graph-logo_no-text.svg")
    );
  }

  ngOnInit(): void {
  }

}
