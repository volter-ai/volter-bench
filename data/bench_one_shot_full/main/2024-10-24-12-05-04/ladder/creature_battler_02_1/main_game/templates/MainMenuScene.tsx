import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react'

interface Player {
    uid: string;
    stats: Record<string, number>;
    meta: Record<string, any>;
    entities: Record<string, any>;
    collections: {
        creatures: Array<{
            uid: string;
            display_name: string;
            description: string;
            stats: Record<string, number>;
        }>;
    };
    display_name: string;
    description: string;
}

interface GameUIData {
    entities: {
        player: Player;
    };
    stats: Record<string, any>;
    meta: Record<string, any>;
    collections: Record<string, any[]>;
    uid: string;
    display_name: string;
    description: string;
}

export function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons()

    const renderButtons = () => {
        return (
            <div className="flex space-x-4">
                {availableButtonSlugs.includes('play') && (
                    <button
                        onClick={() => emitButtonClick('play')}
                        className="flex items-center justify-center px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors"
                    >
                        <Play className="mr-2" size={20} />
                        Play
                    </button>
                )}
                {availableButtonSlugs.includes('quit') && (
                    <button
                        onClick={() => emitButtonClick('quit')}
                        className="flex items-center justify-center px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors"
                    >
                        <X className="mr-2" size={20} />
                        Quit
                    </button>
                )}
            </div>
        );
    };

    return (
        <div className="w-full h-full bg-gradient-to-b from-blue-500 to-purple-600 flex flex-col items-center justify-between p-8" style={{ aspectRatio: '16/9' }}>
            <h1 className="text-4xl md:text-6xl font-bold text-white mt-16">
                {props.data?.display_name || 'Awesome Game'}
            </h1>
            <div className="flex-grow" />
            {renderButtons()}
            {props.data?.entities?.player && (
                <div className="text-white text-sm mt-4">
                    Player: {props.data.entities.player.display_name}
                    {props.data.entities.player.collections?.creatures && props.data.entities.player.collections.creatures.length > 0 && (
                        <span> | First Creature: {props.data.entities.player.collections.creatures[0]?.display_name}</span>
                    )}
                </div>
            )}
        </div>
    );
}
