import { Accordion, AccordionItem, Button, Link, Image } from "@nextui-org/react";
import { get } from "http";


export default function TransformPropertyPage() {
  return (
    <div className="container mx-auto pt-20 h-screen">
    <h1 className="text-4xl font-bold mb-6">Transform a Property</h1>

    <h2 className="text-2xl font-bold mb-4">What can I do?</h2>
    <p>This project focuses on "cleaning and greening" as ways to help reduce gun violence. This includes:</p>
    <ul className="list-disc pl-6 mb-4">
        <li>Removing trash and debris: Cleaning up properties helps make them safe and nice to look at.</li>
        <li>Grading the land: This helps manage water and can stop flooding, making the property better for use.</li>
        <li>Planting trees: A few trees can turn an empty space into a small park, offering shade and a place to relax.</li>
        <li>Installing low fences: Fences about 1 meter high can help keep the space neat and welcoming without closing it off.</li>
        <li>Regular maintenance: This is important to keep the space clean, safe, and nice over time.</li>
    </ul>
    <p>The cost for these kinds of projects is usually low, about $5 per square yard, with maintenance around $0.50 per square yard. Even if you can't do everything, small steps like putting up a fence, planting some trees, or just keeping the area clean can make a big difference.</p>

    <h3 className="text-xl font-bold mt-8 mb-4">Figure out what's right for your property</h3>
    <p>Every property is different. The <a href="https://detroitfuturecity.com/whatwedo/land-use/DFC-lots/" className="text-blue-500 hover:underline">Detroit Future City lot quiz</a> is a good way to start thinking about what could work for your space. Look at things like how much sun the property gets, what kind of soil it has, and what plants are already there. This will help you decide the best way to use the property.</p>

    <h3 className="text-xl font-bold mt-8 mb-4">Remember, there's no one right way</h3>
    <p>Every part of Philadelphia is different and needs different things. It's important to pick a plan that fits your area. Talk to the people who live and work near you, and the leaders in your community. You might find that some places need spaces for families, while others might do well with a garden or places to live that people can afford. It's important to think about how to help people stay in their neighborhoods while also making sure there's enough housing for everyone.</p>

    <h3 className="text-xl font-bold mt-8 mb-4">Be creative</h3>
    <p>Think about other ways you can use empty properties. Besides making parks or gardens, there are lots of options. You could turn a property into a place for outdoor music, a project to help manage rainwater, a place for birds, or an outdoor art space. There are many possibilities, so use your imagination and think about what your community needs most. By being creative, you can help turn these spaces into important and loved parts of your neighborhood.</p>

</div>
  );
}
