import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react';

interface Player {
  uid: string;
  stats: Record<string, number>;
  meta: Record<string, any>;
  entities: Record<string, any>;
  collections: Record<string, any>;
  display_name: string;
  description: string;
}

interface GameUIData {
  entities: {
    player: Player;
  };
  stats: Record<string, any>;
  meta: Record<string, any>;
  collections: Record<string, any>;
}

interface ButtonProps {
  uid: string;
  slug: string;
  onClick: () => void;
  icon: React.ReactNode;
  label: string;
}

const Button: React.FC<ButtonProps> = ({ uid, slug, onClick, icon, label }) => (
  <button
    key={uid}
    onClick={onClick}
    className="flex items-center justify-center px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors duration-200"
  >
    {icon}
    <span className="ml-2">{label}</span>
  </button>
);

export function MainMenuSceneView({ data }: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const buttons = [
    { slug: 'play', icon: <Play size={24} />, label: 'Play' },
    { slug: 'quit', icon: <X size={24} />, label: 'Quit' },
  ];

  return (
    <div className="w-full h-screen flex items-center justify-center bg-gray-900">
      <div className="w-full max-w-[177.78vh] h-full max-h-[56.25vw] bg-gray-800 flex flex-col items-center justify-between p-8">
        <div className="flex-1 flex items-center justify-center">
          <h1 className="text-6xl font-bold text-white text-center">
            {data.meta.game_title || "Game Title"}
          </h1>
        </div>
        <div className="flex space-x-4">
          {buttons.map((button) =>
            availableButtonSlugs.includes(button.slug) ? (
              <Button
                key={`${button.slug}-${Date.now()}`}
                uid={`${button.slug}-${Date.now()}`}
                slug={button.slug}
                onClick={() => emitButtonClick(button.slug)}
                icon={button.icon}
                label={button.label}
              />
            ) : null
          )}
        </div>
      </div>
    </div>
  );
}
