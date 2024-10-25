import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

interface GameUIData {
  entities: {
    player: {
      uid: string;
      display_name: string;
      description: string;
    }
  }
  uid: string;
  display_name: string;
  description: string;
}

export function MainMenuSceneView({ data, uid }: { data: GameUIData; uid: string }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const buttonConfig = {
    play: { text: 'Play', icon: Play },
    quit: { text: 'Quit', icon: X },
  };

  return (
    <Card className="w-full h-full flex flex-col items-center justify-between bg-gradient-to-b from-blue-500 to-purple-600 text-white p-8" uid={uid}>
      <h1 className="text-6xl font-bold mt-16">{data.display_name || 'Game Title'}</h1>
      
      <div className="flex flex-col items-center space-y-4 mb-16">
        {availableButtonSlugs.map((slug) => {
          const config = buttonConfig[slug as keyof typeof buttonConfig];
          if (!config) return null;
          
          const Icon = config.icon;
          return (
            <Button
              key={slug}
              onClick={() => emitButtonClick(slug)}
              className="bg-white text-blue-600 font-semibold py-3 px-6 rounded-full shadow-lg hover:bg-blue-100 transition duration-300 flex items-center space-x-2"
            >
              <Icon className="mr-2" size={24} />
              <span>{config.text}</span>
            </Button>
          );
        })}
      </div>

      <div className="absolute bottom-4 left-4 text-sm opacity-70">
        {data.entities.player?.display_name || 'Unknown Player'}
      </div>
    </Card>
  );
}
