// Do not change these imports:
import { useCurrentButtons } from "@/lib/useChoices.ts";

// Import Lucide icons
import { Play, X } from 'lucide-react';

// Define interfaces for the data structure
interface Player {
  uid: string;
  display_name: string;
  description: string;
}

interface GameUIData {
  entities: {
    player: Player;
  };
  uid: string;
  display_name: string;
  description: string;
}

export function MainMenuSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  // Function to render available buttons
  const renderButtons = () => {
    const buttonConfig = [
      { id: 'play', label: 'Play', icon: <Play className="mr-2" /> },
      { id: 'quit', label: 'Quit', icon: <X className="mr-2" /> },
    ];

    return buttonConfig.map(button => (
      availableButtonSlugs.includes(button.id) && (
        <button
          key={button.id}
          onClick={() => emitButtonClick(button.id)}
          className="flex items-center justify-center px-6 py-3 text-lg font-semibold text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors duration-300"
        >
          {button.icon}
          {button.label}
        </button>
      )
    ));
  };

  // Render the main menu scene
  return (
    <div className="w-full h-screen flex items-center justify-center bg-gray-900">
      <div className="aspect-video max-w-screen-lg w-full h-full bg-gradient-to-b from-blue-500 to-purple-600 flex flex-col justify-between items-center p-8">
        {/* Game title */}
        <h1 className="text-4xl md:text-6xl font-bold text-white mt-16">
          {props.data?.display_name || "Game Title"}
        </h1>
        
        {/* Button container */}
        <div className="flex flex-col space-y-4 mb-16">
          {renderButtons()}
        </div>
      </div>
    </div>
  );
}
