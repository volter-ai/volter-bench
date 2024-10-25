import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

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

export function MainMenuSceneView({ data }: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const buttonConfig = {
    play: { text: "Play", icon: Play },
    quit: { text: "Quit", icon: X },
  };

  return (
    <Card className="w-full h-full flex flex-col items-center justify-between bg-gradient-to-b from-blue-500 to-purple-600 text-white p-8" uid={data.uid}>
      <div className="flex-1 flex items-center justify-center">
        <h1 className="text-6xl font-bold text-center shadow-lg">{data.display_name}</h1>
      </div>
      
      <div className="flex flex-col items-center space-y-4 mb-16">
        {availableButtonSlugs.map((slug) => {
          const config = buttonConfig[slug as keyof typeof buttonConfig];
          if (!config) return null;
          
          return (
            <Button
              key={slug}
              onClick={() => emitButtonClick(slug)}
              className="flex items-center justify-center space-x-2 bg-white text-blue-600 px-8 py-3 rounded-full text-xl font-semibold hover:bg-blue-100 transition-colors duration-200"
              uid={`${data.uid}-${slug}`}
            >
              <config.icon size={24} />
              <span>{config.text}</span>
            </Button>
          );
        })}
      </div>
      
      {data.entities.player && (
        <div className="text-sm text-center">
          <p>Welcome, {data.entities.player.display_name}!</p>
          <p>{data.entities.player.description}</p>
        </div>
      )}
    </Card>
  );
}
