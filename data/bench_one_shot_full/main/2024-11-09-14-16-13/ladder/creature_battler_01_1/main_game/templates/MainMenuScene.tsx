import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, Power } from 'lucide-react';

interface GameStats {
    [key: string]: number;
}

interface GameMeta {
    prototype_id: string;
    category: string;
}

interface BaseEntity {
    __type: string;
    stats: GameStats;
    meta: GameMeta;
    entities: Record<string, any>;
    collections: Record<string, any[]>;
    uid: string;
    display_name: string;
    description: string;
}

interface Player extends BaseEntity {
    __type: "Player";
}

interface GameUIData {
    __type: string;
    stats: GameStats;
    meta: GameMeta;
    entities: {
        player: Player;
    };
    collections: Record<string, any[]>;
    uid: string;
    display_name: string;
    description: string;
}

export function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons();

    if (!props.data) {
        return null;
    }

    return (
        <div className="relative w-full h-0 pb-[56.25%] bg-gradient-to-b from-slate-800 to-slate-900">
            <div className="absolute inset-0 flex flex-col items-center justify-between p-8">
                {/* Title Image Section */}
                <div className="flex-1 flex items-center justify-center w-full max-w-2xl">
                    <div 
                        className="w-full h-48 bg-center bg-contain bg-no-repeat"
                        style={{ backgroundImage: 'url("/game-title.png")' }}
                        aria-label={props.data.display_name || "Game Title"}
                    />
                </div>

                {/* Button Section */}
                <div className="flex flex-col gap-4 mb-16 w-full max-w-md">
                    {availableButtonSlugs?.includes('play') && (
                        <button
                            onClick={() => emitButtonClick('play')}
                            className="flex items-center justify-center gap-2 px-8 py-4 text-xl 
                                     bg-green-600 hover:bg-green-500 text-white rounded-lg 
                                     transition-colors duration-200 w-full"
                        >
                            <Play size={24} />
                            <span>Play Game</span>
                        </button>
                    )}

                    {availableButtonSlugs?.includes('quit') && (
                        <button
                            onClick={() => emitButtonClick('quit')}
                            className="flex items-center justify-center gap-2 px-8 py-4 text-xl 
                                     bg-red-600 hover:bg-red-500 text-white rounded-lg 
                                     transition-colors duration-200 w-full"
                        >
                            <Power size={24} />
                            <span>Quit</span>
                        </button>
                    )}
                </div>
            </div>
        </div>
    );
}
