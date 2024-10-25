import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react'

interface Player {
  uid: string;
  display_name: string;
}

interface GameUIData {
  entities: {
    player: Player;
  };
}

export function MainMenuSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const playerName = props.data.entities.player?.display_name || "Player";

  const buttonConfig = {
    play: { text: "Play", icon: Play },
    quit: { text: "Quit", icon: X },
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-b from-blue-500 to-purple-600">
      <div className="w-full max-w-4xl aspect-w-16 aspect-h-9 bg-black bg-opacity-50 flex flex-col justify-between p-8">
        <div className="text-center">
          <h1 className="text-4xl md:text-6xl font-bold text-white mb-4">Creature Battle</h1>
          <p className="text-xl text-white">Welcome, {playerName}!</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {availableButtonSlugs.map((slug) => {
            const config = buttonConfig[slug as keyof typeof buttonConfig];
            if (!config) return null;

            return (
              <button
                key={slug}
                onClick={() => emitButtonClick(slug)}
                className="flex items-center justify-center bg-white bg-opacity-20 hover:bg-opacity-30 text-white py-3 px-6 rounded-lg transition duration-300"
              >
                <config.icon className="mr-2" size={24} />
                {config.text}
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
}
