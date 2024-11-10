import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react';

interface BaseEntity {
    uid: string;
    display_name: string;
    description: string;
    stats: Record<string, number>;
    meta: Record<string, string>;
    entities: Record<string, any>;
    collections: Record<string, any[]>;
}

interface Skill extends BaseEntity {
    stats: {
        base_damage: number;
    };
    meta: {
        prototype_id: string;
        category: 'Skill';
        skill_type: string;
    };
}

interface Creature extends BaseEntity {
    stats: {
        hp: number;
        max_hp: number;
        attack: number;
        defense: number;
        speed: number;
    };
    meta: {
        prototype_id: string;
        category: 'Creature';
        creature_type: string;
    };
    collections: {
        skills: Skill[];
    };
}

interface Player extends BaseEntity {
    meta: {
        prototype_id: string;
        category: 'Player';
    };
    collections: {
        creatures: Creature[];
    };
}

interface GameUIData extends BaseEntity {
    meta: {
        category: 'MainMenuScene';
    };
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
        <div className="w-full h-full relative bg-gradient-to-b from-slate-900 to-slate-800">
            {/* 16:9 Aspect Ratio Container */}
            <div className="absolute inset-0 flex flex-col items-center justify-between py-12">
                {/* Title Section */}
                <div className="flex-1 flex items-center justify-center">
                    <h1 className="text-6xl font-bold text-white tracking-wider">
                        {props.data?.display_name || 'GAME TITLE'}
                    </h1>
                </div>

                {/* Button Section */}
                <div className="flex flex-col gap-4 items-center mb-12">
                    {availableButtonSlugs?.includes('play') && (
                        <button
                            onClick={() => emitButtonClick('play')}
                            className="flex items-center gap-2 px-8 py-4 bg-emerald-600 hover:bg-emerald-500 
                                     text-white rounded-lg text-xl font-semibold transition-colors"
                        >
                            <Play size={24} />
                            Play Game
                        </button>
                    )}

                    {availableButtonSlugs?.includes('quit') && (
                        <button
                            onClick={() => emitButtonClick('quit')}
                            className="flex items-center gap-2 px-8 py-4 bg-red-600 hover:bg-red-500 
                                     text-white rounded-lg text-xl font-semibold transition-colors"
                        >
                            <X size={24} />
                            Quit
                        </button>
                    )}
                </div>
            </div>
        </div>
    );
}
