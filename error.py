import math

def error_flux(tijd, Solid, Aeff, hoek_graad, N, d, h, b, l, w, le, Err_h, Err_d):
    hoek = hoek_graad*math.pi/180
    cos_hoek = math.cos(hoek)
    sin_hoek = math.sin(hoek)
    sec_hoek = 1/(math.cos(hoek))
    tan_hoek = math.tan(hoek)

    Err_N = math.sqrt(N)
    par_flux_N = 1/(tijd*Solid*Aeff)

    par_hoek_h = -d/(d^2+h^2)

    par_hoek_d = h/(d^2+h^2)

    Err_hoek = math.sqrt((Err_d*par_hoek_d)**2+(Err_h*par_hoek_h)**2)
    par_Aeff_hoek = (-b*sin_hoek*(l+h))

    Err_Aeff = abs(Err_hoek*par_Aeff_hoek)
    par_flux_Aeff = -N/(tijd*Solid*(Aeff**2))

    par_Solid_hoek = (4*h*le*w*cos_hoek*((w**2 + h**2)*cos_hoek**2 + le**2)*sin_hoek)/((h**2*cos_hoek**2 + le**2) * (w**2*cos_hoek**2 + h**2*cos_hoek**2 + le**2)**(1.5))
    par_Solid_hoek_num = 2*h*le*w*sec_hoek*((h**2*sec_hoek**2 + 4*w**2*cos_hoek**2 + 4*le**2)*((2*h**2*cos_hoek*sec_hoek**2 + 4*w**2*cos_hoek**3 + 4*le**2*cos_hoek)*tan_hoek + (h**2*sec_hoek**2 + 4*le**2)*sin_hoek))
    par_Solid_hoek_den = (((h**2*sec_hoek**2)/4 + w**2*cos_hoek**2 + le**2)**(3/2) * (h**4*sec_hoek**4 + (4*h**2*w**2*cos_hoek**2 + 4*h**2*le**2)*sec_hoek**2 + 16*le**2*w**2*cos_hoek**2))
    par_Solid_hoek = - par_Solid_hoek_num/par_Solid_hoek_den
    #par_Solid_le = (4*h*cos_hoek**2*w)/((le**2 + h**2*cos_hoek**2)*math.sqrt(le**2 + cos_hoek**2*w**2 + h**2*cos_hoek**2))
    #par_Solid_w = (4*h*le)/((w**2 + h**2)*math.sqrt((w**2 + h**2) * cos_hoek**2 + le**2))
    #par_Solid_h = -(4*le*w*(2*cos_hoek**2*h**2 + cos_hoek**2*w**2 + le**2))/(math.sqrt(cos_hoek**2*h**2 + cos_hoek**2*w**2 + le**2)(cos_hoek**2*h**4 + (cos_hoek**2*w**2 + le**2)*h**2 + le**2*w**2))
    par_Solid_h = -(32*le*w*cos_hoek*sec_hoek*(sec_hoek**2*h**2 + 2*(cos_hoek**2*w**2 + le**2)))/(math.sqrt(sec_hoek**2*h**2 + 4*(cos_hoek**2*w**2 + le**2))*(sec_hoek**2*h**2 + 4*le**2)*(sec_hoek**2*h**2 + 4*cos_hoek**2*w**2))

    Err_Solid = math.sqrt((Err_hoek*par_Solid_hoek)**2+(Err_h*par_Solid_h)**2)
    par_flux_Solid = -(N/(tijd*Solid**2*Aeff))

    Err_flux = math.sqrt((Err_N*par_flux_N)**2+(Err_Aeff*par_flux_Aeff)**2+(Err_Solid*par_flux_Solid)**2)
    return Err_flux
