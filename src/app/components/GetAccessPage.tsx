import { Accordion, AccordionItem, Button, Link, Image } from "@nextui-org/react";
import { get } from "http";


export default function GetAccessPage() {
  return (
    <div className="container mx-auto pt-20 h-screen">
    <h1 className="text-4xl font-bold mb-6">Get Access</h1>

    <h2 className="text-2xl font-bold mt-8">Where can I get help?</h2>
    <h3 className="text-xl font-bold mt-8 mb-4">Community Groups and Local Representatives</h3>
    <p>For help with greening projects, reach out to local Neighborhood Advisory Committees, Community Development Corporations, or Registered Community Organizations. They can guide you through the planning process and help with local rules. Local representatives can also support you, especially if you're facing red tape. Bring them a solid plan and show how your project can improve the community.</p>

    <h3 className="text-xl font-bold mt-8 mb-4">Garden Justice Legal Initiative</h3>
    <p>The <a href="https://pubintlaw.org/cases-and-projects/garden-justice-legal-initiative-gjli/" className="text-blue-500 hover:underline">Garden Justice Legal Initiative</a> supports community gardens and urban farms, offering free legal help, policy research, and community education. They work with coalitions like <a href="https://soilgeneration.org/" className="text-blue-500 hover:underline">Soil Generation</a> to empower residents to use vacant land for gardens and farming, providing tools and information through training sessions and their online resource, <a href="https://groundedinphilly.org/" className="text-blue-500 hover:underline">Grounded in Philly</a>.</p>

    <h3 className="text-xl font-bold mt-8 mb-4">The Land Bank/PHDC</h3>
    <p>The <a href="https://phdcphila.org/land/" className="text-blue-500 hover:underline">Philadelphia Land Bank</a>, run by PHDC, makes it easier to get vacant land for community use. They streamline the process of acquiring public land and offer it for uses like community gardens, affordable housing, and business expansion. They offer free or heavily discounted property for approved, community-oriented uses.</p>

    <h3 className="text-xl font-bold mt-8 mb-4">StreetBoxPHL</h3>
    <p><a href="https://streetboxphl.com/" className="text-blue-500 hover:underline">StreetBoxPHL</a> helps community groups revitalize urban spaces by making parklets, pedestrian plazas, and bike corrals. Their tools can quickly transform underused spaces into vibrant, green areas that benefit the whole community. They offer technical support, a street furniture library, and help with insurance requirements.</p>

    <h3 className="text-xl font-bold mt-8 mb-4">Park in a Truck</h3>
    <p><a href="https://www.jefferson.edu/academics/colleges-schools-institutes/architecture-and-the-built-environment/programs/landscape-architecture/park-in-a-truck.html" className="text-blue-500 hover:underline">Park in a Truck</a> supports community residents in quickly building custom parks. They've developed <a href="https://www.jefferson.edu/content/dam/academic/cabe/landscape-architecture/park-in-a-truck/toolkit/PiaT-toolkit-2022.pdf" className="text-blue-500 hover:underline">a toolkit</a> that helps community groups design and build parks that fit their needs. They also offer training and technical support to help communities create and maintain their parks.</p>

    <h2 className="text-2xl font-bold mt-8 mb-4">Things to Keep in Mind</h2>
    <h3 className="text-xl font-bold mt-8 mb-4">Funding</h3>
    <p>When it comes to funding, try to connect with local businesses and community groups. Small grants and donations might be easier to get for groups like yours. And don't forget about raising money right in the community through events or online campaigns.</p>

    <h3 className="text-xl font-bold mt-8 mb-4">Maintenance</h3>
    <p>It's also key to make sure that the improvements you make can keep going for a long time. Getting people in the area to care about and look after these spaces can really help. Choose projects that don't cost much but still have a big impact, so they're easier for the community to maintain. Be smart about legal stuff, especially with private property, and work with local authorities to make sure everything is okay there.</p>

    <h3 className="text-xl font-bold mt-8 mb-4">Gentrification</h3>
    <p>Remember, your projects shouldn't push out the current residents. Keep them at the heart of what you do, and keep an eye on how things change in the neighborhood. Work together with other local groups, schools, and businesses - it's a great way to get more resources and ideas. Have regular meetings with people in the community to keep them in the loop and involved in decisions.</p>
</div>
  );
}
