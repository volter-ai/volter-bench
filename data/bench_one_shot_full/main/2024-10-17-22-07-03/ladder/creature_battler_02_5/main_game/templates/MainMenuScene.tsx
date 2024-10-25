import { useCurrentButtons, useThingInteraction } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react';

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

const Button = ({ slug, onClick, icon: Icon, label }: { slug: string; onClick: () => void; icon: React.ElementType; label: string }) => (
  <button
    onClick={onClick}
    className="flex items-center justify-center px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors duration-200"
  >
    <Icon className="mr-2" size={20} />
    {label}
  </button>
);

export function MainMenuSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();
  const { enabledUIDs } = useThingInteraction();

  const handleButtonClick = (slug: string) => {
    emitButtonClick(slug);
  };

  return (
    <div className="w-full h-full flex items-center justify-center bg-gradient-to-b from-purple-800 to-indigo-900">
      <div className="w-full max-w-[177.78vh] h-full max-h-[56.25vw] flex flex-col items-center justify-between py-12">
        <h1 className="text-6xl font-bold text-white mb-8">Game Title</h1>
        
        <div className="flex flex-col items-center space-y-4">
          {availableButtonSlugs.includes('play') && (
            <Button
              slug="play"
              onClick={() => handleButtonClick('play')}
              icon={Play}
              label="Play"
            />
          )}
          {availableButtonSlugs.includes('quit') && (
            <Button
              slug="quit"
              onClick={() => handleButtonClick('quit')}
              icon={X}
              label="Quit"
            />
          )}
        </div>
      </div>
    </div>
  );
}
