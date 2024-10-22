import { useCurrentButtons, useThingInteraction } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react'
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
  stats: Record<string, number>;
  meta: Record<string, any>;
  uid: string;
}

export function MainMenuSceneView({ data }: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const {
    enabledUIDs
  } = useThingInteraction()

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
          className="w-full mb-4"
        >
          {button.icon}
          {button.label}
        </Button>
      )
    ));
  };

  return (
    <div className="w-full h-screen bg-gradient-to-b from-blue-900 to-purple-900 flex flex-col items-center justify-between p-8" style={{ aspectRatio: '16/9' }}>
      <div className="flex-1 flex items-center justify-center">
        <h1 className="text-6xl font-bold text-white text-center mb-8">
          {data?.entities?.player?.display_name || "Game Title"}
        </h1>
      </div>
      <div className="flex flex-col items-center w-64">
        {renderButtons()}
      </div>
    </div>
  );
}
