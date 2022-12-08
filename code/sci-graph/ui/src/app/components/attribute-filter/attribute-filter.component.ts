import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { MatCheckboxChange } from '@angular/material/checkbox';
import { AttributeResponse } from 'src/app/model/responses';
import { FilterService } from 'src/app/services/filter.service';

@Component({
  selector: 'app-attribute-filter',
  templateUrl: './attribute-filter.component.html',
  styleUrls: ['./attribute-filter.component.scss']
})
export class AttributeFilterComponent{

  @Input() attribute: AttributeResponse = {attribute_name: 'undefined', values: ['no value available']};
  @Output() filterChangedEvent = new EventEmitter();

  currentValue: string = "";
  anyCheckboxChecked: boolean = false;
  settingFilterFailed: boolean = false;

  constructor (
    private filterService: FilterService,
  ) {}

  checked(event: MatCheckboxChange, value: string): void{
    if (event.checked){
      this.anyCheckboxChecked = true;
      this.currentValue = value;
      this.filterService.setAttributeFilter(this.attribute.attribute_name, value).subscribe({
        error: (e) => {
          this.settingFilterFailed = true;
        },
        complete: () => {
          this.settingFilterFailed = false;
          this.filterChangedEvent.emit();
        }
      });
      return;
    }
    this.anyCheckboxChecked = false;
    this.filterService.deleteAttributeFilter(this.attribute.attribute_name).subscribe({
      error: (e) => {
        this.settingFilterFailed = true;
      },
      complete: () => {
        this.settingFilterFailed = false;
        this.filterChangedEvent.emit();
      }
    })
  }

  checkboxDisabled(value: string){
    return (this.anyCheckboxChecked && value !== this.currentValue);
  }

}
