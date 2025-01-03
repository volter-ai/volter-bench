import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import { Card as ShadcnCard, CardHeader as ShadcnCardHeader, CardTitle as ShadcnCardTitle, CardContent as ShadcnCardContent } from "@/components/ui/card"

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string;
  name: string;
  imageUrl: string;
  hp: number;
  maxHp: number;
}

let Card = withClickable(React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement> & { uid: string }>(
  ({ uid, ...props }, ref) => <ShadcnCard ref={ref} {...props} />
))

let CardHeader = withClickable(React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement> & { uid: string }>(
  ({ uid, ...props }, ref) => <ShadcnCardHeader ref={ref} {...props} />
))

let CardTitle = withClickable(React.forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLHeadingElement> & { uid: string }>(
  ({ uid, ...props }, ref) => <ShadcnCardTitle ref={ref} {...props} />
))

let CardContent = withClickable(React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement> & { uid: string }>(
  ({ uid, ...props }, ref) => <ShadcnCardContent ref={ref} {...props} />
))

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, imageUrl, hp, maxHp, ...props }, ref) => (
    <Card uid={`${uid}-card`} ref={ref} className={cn("w-64", className)} {...props}>
      <CardHeader uid={`${uid}-header`}>
        <CardTitle uid={`${uid}-title`}>{name}</CardTitle>
      </CardHeader>
      <CardContent uid={`${uid}-content`}>
        <img src={imageUrl} alt={name} className="w-full h-40 object-cover mb-4" />
        <div>HP: {hp}/{maxHp}</div>
      </CardContent>
    </Card>
  )
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
