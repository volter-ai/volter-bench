import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, Power } from 'lucide-react';

interface Stats {
    hp?: number;
    max_hp?: number;
    attack?: number;
    defense?: number;
    sp_attack?: number;
    sp_defense?: number;
    speed?: number;
    base_damage?: number;
}

interface Meta {
    prototype_id: string;
    category: string;
    creature_type?: string;
    skill_type?: string;
    is_physical?: boolean;
}

interface BaseEntity {
    __type: string;
    uid: string;
    display_name: string;
    description: string;
    stats: Stats;
    meta: Meta;
    entities: Record<string, any>;
    collections: Record<string, any[]>;
}

interface Skill extends BaseEntity {
    __type: 'Skill';
}

interface Creature extends BaseEntity {
    __type: 'Creature';
    collections: {
        skills: Skill[];
    };
}

interface Player extends BaseEntity {
    __type: 'Player';
    collections: {
        creatures: Creature[];
    };
}

interface GameUIData {
    entities: {
        player: Player;
    };
}

export function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons();

    return (
        <div className="w-full h-full relative bg-slate-900">
            <div className="relative w-full pb-[56.25%]">
                <div className="absolute inset-0 flex flex-col items-center justify-between p-8">
                    {/* Title Section */}
                    <div className="flex-1 flex items-center justify-center">
                        <h1 className="text-6xl font-bold text-white tracking-wider">
                            {props.data?.entities?.player?.display_name ?? 'GAME TITLE'}
                        </h1>
                    </div>

                    {/* Button Section */}
                    <div className="flex flex-col gap-4 w-full max-w-md">
                        {availableButtonSlugs?.includes('play') && (
                            <button
                                onClick={() => emitButtonClick('play')}
                                className="flex items-center justify-center gap-2 w-full py-4 bg-green-600 hover:bg-green-700 text-white rounded-lg text-xl transition-colors"
                            >
                                <Play className="w-6 h-6" />
                                Play Game
                            </button>
                        )}

                        {availableButtonSlugs?.includes('quit') && (
                            <button
                                onClick={() => emitButtonClick('quit')}
                                className="flex items-center justify-center gap-2 w-full py-4 bg-red-600 hover:bg-red-700 text-white rounded-lg text-xl transition-colors"
                            >
                                <Power className="w-6 h-6" />
                                Quit
                            </button>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}
