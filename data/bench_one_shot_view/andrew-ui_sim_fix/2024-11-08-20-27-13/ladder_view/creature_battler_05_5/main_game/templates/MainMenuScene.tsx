import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, Power } from 'lucide-react';
import { Button } from "@/components/ui/button";

interface Stats {
    hp?: number;
    max_hp?: number;
    attack?: number;
    defense?: number;
    sp_attack?: number;
    sp_defense?: number;
    speed?: number;
}

interface Meta {
    prototype_id: string;
    category: string;
}

interface BaseEntity {
    __type: string;
    stats: Stats;
    meta: Meta;
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

    return (
        <div className="w-full h-full flex flex-col items-center justify-between bg-gradient-to-b from-slate-900 to-slate-800 aspect-video">
            <div className="flex-1 flex items-center justify-center pt-16">
                <h1 className="text-6xl font-bold text-white tracking-wider">
                    CREATURE BATTLE
                </h1>
            </div>

            <div className="flex flex-col gap-4 mb-16">
                {availableButtonSlugs.includes('play') && (
                    <Button
                        onClick={() => emitButtonClick('play')}
                        className="flex items-center justify-center gap-2 px-8 py-6 text-xl"
                        size="lg"
                        variant="default"
                    >
                        <Play className="w-6 h-6" />
                        Play Game
                    </Button>
                )}

                {availableButtonSlugs.includes('quit') && (
                    <Button
                        onClick={() => emitButtonClick('quit')}
                        className="flex items-center justify-center gap-2 px-8 py-6 text-xl"
                        size="lg"
                        variant="destructive"
                    >
                        <Power className="w-6 h-6" />
                        Quit
                    </Button>
                )}
            </div>
        </div>
    )
}
