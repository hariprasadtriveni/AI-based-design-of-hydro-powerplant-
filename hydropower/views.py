from django.shortcuts import render, get_object_or_404
from  .models import HydroPowerDesign
import openai

# Create your views here.
def index(request):
    return render(request, "index.html")

def generate_design(request):
    if request.method == "POST":
        location = request.POST['location']
        river_flow = float(request.POST['river_flow'])
        budget = float(request.POST['budget'])
        power_requirement = float(request.POST['power_requirement'])

        # Create and save design entry
        design = HydroPowerDesign.objects.create(
            location=location,
            river_flow=river_flow,
            budget=budget,
            power_requirement=power_requirement
        )
        request.session['design_id'] = design.id  # Store ID in session
        request.session.modified = True  # Ensure session updates
        return render(request, "sections.html")

def generate_ai_content(prompt, **kwargs):
    formatted_prompt = prompt.format(**kwargs)
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": formatted_prompt}],
    )
    content = response["choices"][0]["message"]["content"]
    return "\n".join([f"- {point.strip()}" for point in content.split("\n") if point.strip()])

def generate_dalle_image(prompt, **kwargs):
    formatted_prompt = prompt.format(**kwargs)
    response = openai.Image.create(
        model="dall-e-3",
        prompt=formatted_prompt, 
        size="1792x1024"
    )
    return response["data"][0]["url"]

def civil_structure(request):
    design_id = request.session.get('design_id')
    if not design_id:
        return render(request, "error.html", {"message": "Design session not found!"})
    
    design = get_object_or_404(HydroPowerDesign, id=design_id)
    text_prompt = (
        "Generate a civil structure design for a hydro power plant in {location} "
        "with river flow of {river_flow} cubic meters per second, "
        "a budget of {budget} million dollars, "
        "and a power requirement of {power_requirement} MW."
    )
    image_prompt = (
        "A detailed civil engineering blueprint of a hydro power plant in {location}, "
        "including dam, intake, and penstocks, designed for {power_requirement} MW capacity."
    )
    
    civil_text = generate_ai_content(text_prompt, location=design.location, 
                                     river_flow=design.river_flow, budget=design.budget, 
                                     power_requirement=design.power_requirement)
    
    civil_image = generate_dalle_image(image_prompt, location=design.location, 
                                       power_requirement=design.power_requirement)
    
    design.civil_design_text = civil_text
    design.civil_design_image = civil_image
    design.save()
    
    return render(request, "civil.html", {"data": civil_text, "image_url": civil_image})

def hydroelectric_system(request):
    design_id = request.session.get('design_id')
    if not design_id:
        return render(request, "error.html", {"message": "Design session not found!"})
    
    design = get_object_or_404(HydroPowerDesign, id=design_id)
    text_prompt = (
        "Generate a hydroelectric system design for a hydro power plant in {location}, "
        "designed for {power_requirement} MW output with an estimated budget of {budget} million dollars."
    )
    image_prompt = (
        "A realistic hydroelectric power generation system in {location}, featuring turbines and generators "
        "inside a power station, optimized for {power_requirement} MW capacity."
    )
    
    hydro_text = generate_ai_content(text_prompt, location=design.location, 
                                     budget=design.budget, power_requirement=design.power_requirement)
    
    hydro_image = generate_dalle_image(image_prompt, location=design.location, 
                                       power_requirement=design.power_requirement)
    
    design.hydroelectric_text = hydro_text
    design.hydroelectric_image = hydro_image
    design.save()
    
    return render(request, "hydroelectric.html", {"data": hydro_text, "image_url": hydro_image})

def mechanical_components(request):
    design_id = request.session.get('design_id')
    if not design_id:
        return render(request, "error.html", {"message": "Design session not found!"})
    
    design = get_object_or_404(HydroPowerDesign, id=design_id)
    text_prompt = (
        "Generate mechanical component details for a hydro power plant in {location} with "
        "a power capacity of {power_requirement} MW. Describe the key mechanical systems involved."
    )
    image_prompt = (
        "High-quality illustration of mechanical components like turbines, transformers, and penstocks "
        "used in a hydro power plant in {location}, designed for {power_requirement} MW generation."
    )
    
    mech_text = generate_ai_content(text_prompt, location=design.location, 
                                    power_requirement=design.power_requirement)
    
    mech_image = generate_dalle_image(image_prompt, location=design.location, 
                                      power_requirement=design.power_requirement)
    
    design.mechanical_text = mech_text
    design.mechanical_image = mech_image
    design.save()
    
    return render(request, "mechanical.html", {"data": mech_text, "image_url": mech_image})
