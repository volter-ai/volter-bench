import { useCurrentButtons, useThingInteraction } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react';
import { Button } from "@/components/ui/button";

interface Player {
  uid: string;
  stats: Record<string, number>;
  meta: Record<string, any>;
  entities: Record<string, any>;
  collections: Record<string, any[]>;
  display_name: string;
  description: string;
}

interface GameUIData {
  entities: {
    player: Player;
  };
  stats: Record<string, any>;
  meta: Record<string, any>;
}

export function MainMenuSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const {
    enabledUIDs
  } = useThingInteraction();

  const renderButtons = () => {
    const buttons = [
      { id: 'play', label: 'Play', icon: <Play className="mr-2 h-4 w-4" /> },
      { id: 'quit', label: 'Quit', icon: <X className="mr-2 h-4 w-4" /> },
    ];

    return buttons.map(button => (
      availableButtonSlugs.includes(button.id) && (
        <Button
          key={button.id}
          onClick={() => emitButtonClick(button.id)}
          className="w-full max-w-xs mb-4"
        >
          {button.icon}
          {button.label}
        </Button>
      )
    ));
  };

  return (
    <div className="w-full h-screen bg-gradient-to-b from-blue-500 to-purple-600 flex flex-col items-center justify-between py-12">
      <div className="w-full max-w-7xl aspect-video bg-black bg-opacity-50 rounded-lg shadow-lg flex flex-col items-center justify-between p-8">
        <h1 className="text-4xl md:text-6xl font-bold text-white mb-8">
          {props.data.entities.player?.display_name || "Game Title"}
        </h1>
        <div className="flex flex-col items-center">
          {renderButtons()}
        </div>
      </div>
    </div>
  );
}
