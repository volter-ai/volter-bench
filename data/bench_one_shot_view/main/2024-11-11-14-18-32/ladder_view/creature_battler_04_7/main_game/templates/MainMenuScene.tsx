import {useCurrentButtons} from "@/lib/useChoices.ts";
import {Play, XCircle} from 'lucide-react'

interface GameStats {
    [key: string]: number;
}

interface GameMeta {
    prototype_id: string;
    category: string;
    [key: string]: string;
}

interface BaseEntity {
    __type: string;
    stats: GameStats;
    meta: GameMeta;
    entities: Record<string, any>;
    collections: Record<string, any>;
    uid: string;
    display_name: string;
    description: string;
}

interface Player extends BaseEntity {
    __type: "Player";
}

interface GameUIData {
    entities: {
        player: Player;
    }
}

export function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons()

    const buttonConfig = {
        play: { icon: Play, label: "Play Game" },
        quit: { icon: XCircle, label: "Quit Game" }
    }

    return (
        <div className="w-full h-full aspect-video bg-gradient-to-b from-slate-900 to-slate-800 flex flex-col items-center justify-between p-8">
            <div className="flex-1 flex items-center justify-center">
                <h1 className="text-6xl font-bold text-white tracking-wider">
                    Game Title
                </h1>
            </div>

            <div className="flex flex-col gap-y-4 items-center mb-12">
                {Object.entries(buttonConfig).map(([slug, config]) => {
                    if (!availableButtonSlugs.includes(slug)) return null;
                    
                    const Icon = config.icon;
                    
                    return (
                        <button
                            key={slug}
                            onClick={() => emitButtonClick(slug)}
                            className="flex items-center gap-x-2 px-8 py-4 bg-slate-700 hover:bg-slate-600 
                                     text-white rounded-lg transition-colors duration-200"
                        >
                            <Icon className="w-5 h-5" />
                            <span>{config.label}</span>
                        </button>
                    );
                })}
            </div>
        </div>
    )
}
