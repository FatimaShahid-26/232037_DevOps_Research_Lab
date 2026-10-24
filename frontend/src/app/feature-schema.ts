export type Feature = {name:string; label:string; min?:number; max?:number};
export const FEATURES:Feature[]=[
 {name:'elevation_m',label:'Elevation (metres)',min:-500,max:9000},
 {name:'slope_deg',label:'Slope (degrees)',min:0,max:90},
 {name:'aspect_deg',label:'Aspect (degrees)',min:0,max:359.999},
 {name:'temp_mean_c',label:'Annual mean temperature (°C)',min:-50,max:60},
 {name:'precip_total_mm',label:'Annual precipitation (mm)',min:0,max:15000}
];
