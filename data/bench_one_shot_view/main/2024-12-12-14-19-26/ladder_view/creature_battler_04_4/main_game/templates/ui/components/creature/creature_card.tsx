import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import { 
  Card as ShadcnCard, 
  CardContent as ShadcnCardContent, 
  CardHeader as ShadcnCardHeader, 
  CardTitle as ShadcnCardTitle 
} from "@/components/ui/card"
import { Progress as ShadcnProgress } from "@/components/ui/progress"

interface BaseProps {
  uid: string
}

let Card = React.forwardRef<HTMLDivElement, React.ComponentProps<typeof ShadcnCard> & BaseProps>(
  ({ uid, ...props }, ref) => <ShadcnCard ref={ref} {...props} />
)

let CardContent = React.forwardRef<HTMLDivElement, React.ComponentProps<typeof ShadcnCardContent> & BaseProps>(
  ({ uid, ...props }, ref) => <ShadcnCardContent ref={ref} {...props} />
)

let CardHeader = React.forwardRef<HTMLDivElement, React.ComponentProps<typeof ShadcnCardHeader> & BaseProps>(
  ({ uid, ...props }, ref) => <ShadcnCardHeader ref={ref} {...props} />
)

let CardTitle = React.forwardRef<HTMLHeadingElement, React.ComponentProps<typeof ShadcnCardTitle> & BaseProps>(
  ({ uid, ...props }, ref) => <ShadcnCardTitle ref={ref} {...props} />
)

let Progress = React.forwardRef<HTMLDivElement, React.ComponentProps<typeof ShadcnProgress> & BaseProps>(
  ({ uid, ...props }, ref) => <ShadcnProgress ref={ref} {...props} />
)

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  image: string
  currentHp: number
  maxHp: number
}

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, image, currentHp, maxHp, ...props }, ref) => {
    return (
      <Card uid={uid} ref={ref} className={cn("w-[300px]", className)} {...props}>
        <CardHeader uid={`${uid}-header`}>
          <CardTitle uid={`${uid}-title`}>{name}</CardTitle>
        </CardHeader>
        <CardContent uid={`${uid}-content`}>
          <div className="flex flex-col gap-4">
            <img
              src={image}
              alt={name}
              className="h-[200px] w-full object-contain"
            />
            <div className="space-y-2">
              <div className="flex justify-between">
                <span>HP</span>
                <span>{`${currentHp}/${maxHp}`}</span>
              </div>
              <Progress uid={`${uid}-progress`} value={(currentHp / maxHp) * 100} />
            </div>
          </div>
        </CardContent>
      </Card>
    )
  }
)

Card.displayName = "Card"
CardContent.displayName = "CardContent"
CardHeader.displayName = "CardHeader"
CardTitle.displayName = "CardTitle"
Progress.displayName = "Progress"
CreatureCard.displayName = "CreatureCard"

Card = withClickable(Card)
CardContent = withClickable(CardContent)
CardHeader = withClickable(CardHeader)
CardTitle = withClickable(CardTitle)
Progress = withClickable(Progress)
CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
